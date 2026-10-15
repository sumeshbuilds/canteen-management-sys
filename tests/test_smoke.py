"""Smoke tests for the current demo workflows.

Written with the stdlib ``unittest`` so they run with zero extra
dependencies::

    python -m unittest discover -s tests -v

They are pytest-compatible too (``pip install -r requirements-dev.txt``
then ``pytest``), which is the testing standard from Phase 1 onwards.
"""
import tempfile
import unittest
from pathlib import Path

from config import TestingConfig
from app import create_app


class CanteenAppTestCase(unittest.TestCase):
    """Base case: a fresh app backed by a throwaway database per test."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        config = type(
            "TestConfig",
            (TestingConfig,),
            {"DATABASE_FILE": Path(self._tmpdir.name) / "test.db"},
        )
        self.app = create_app(config)
        self.client = self.app.test_client()

    def tearDown(self):
        self._tmpdir.cleanup()


class MenuTests(CanteenAppTestCase):
    def test_menu_lists_seeded_items(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Veg Sandwich", response.data)
        self.assertIn(b"8 items available", response.data)


class OrderTests(CanteenAppTestCase):
    def test_place_order_creates_order_and_calculates_total(self):
        response = self.client.post(
            "/place-order",
            data={
                "student_name": "Test Student",
                "student_id": "CS-01",
                "item_id": ["1"],  # Veg Sandwich, 35.00
                "quantity": ["2"],
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Order #1", response.data)
        self.assertIn(b"70.00", response.data)

    def test_place_order_without_items_is_rejected(self):
        response = self.client.post(
            "/place-order",
            data={
                "student_name": "Test Student",
                "student_id": "CS-01",
                "item_id": ["1"],
                "quantity": ["0"],
            },
            follow_redirects=True,
        )
        self.assertIn(b"Choose at least one item", response.data)

    def test_place_order_requires_student_details(self):
        response = self.client.post(
            "/place-order",
            data={"student_name": "", "student_id": "", "item_id": ["1"], "quantity": ["1"]},
            follow_redirects=True,
        )
        self.assertIn(b"Please enter your name and student ID", response.data)

    def test_order_total_ignores_browser_supplied_price(self):
        """The server must price the order itself, not trust the client."""
        response = self.client.post(
            "/place-order",
            data={
                "student_name": "Test Student",
                "student_id": "CS-01",
                "item_id": ["1"],
                "quantity": ["1"],
                "price": ["9999"],  # ignored: no such field is read
                "total": ["1.00"],  # ignored
            },
            follow_redirects=True,
        )
        self.assertIn(b"35.00", response.data)
        self.assertNotIn(b"9999", response.data)


class TrackingTests(CanteenAppTestCase):
    def test_unknown_order_shows_not_found(self):
        response = self.client.post(
            "/order-status", data={"order_id": "9999"}, follow_redirects=True
        )
        self.assertIn(b"No order found", response.data)


class AdminTests(CanteenAppTestCase):
    def test_dashboard_loads(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin dashboard", response.data)

    def test_add_menu_item(self):
        self.client.post(
            "/admin",
            data={"action": "add_item", "name": "Masala Dosa", "category": "Breakfast", "price": "45"},
            follow_redirects=True,
        )
        response = self.client.get("/")
        self.assertIn(b"Masala Dosa", response.data)


if __name__ == "__main__":
    unittest.main()
