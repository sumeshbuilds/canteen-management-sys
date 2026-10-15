"""Current (temporary) data-access layer.

The prototype persists everything in a single SQLite file using the
stdlib ``sqlite3`` driver. This module is the only place that knows the
database path and the raw schema, so that the eventual swap to
SQLAlchemy (Phase 1, see BUILD_PLAN.md) touches one file.

Rules for maintainers:
  * Keep all raw SQL confined to this module and the blueprints.
  * Every connection enables ``PRAGMA foreign_keys`` explicitly.
"""
import sqlite3

from pathlib import Path

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    available INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Received',
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY(menu_item_id) REFERENCES menu_items(id) ON DELETE SET NULL
);
"""

SEED_MENU = [
    ("Veg Sandwich", "Snacks", 35),
    ("Samosa", "Snacks", 15),
    ("Veg Noodles", "Meals", 50),
    ("Fried Rice", "Meals", 60),
    ("Tea", "Beverages", 10),
    ("Coffee", "Beverages", 20),
    ("Idli (2 pcs)", "Breakfast", 25),
    ("Veg Roll", "Snacks", 30),
]


def db_path() -> Path:
    """Return the configured database file path."""
    configured = current_app.config.get("DATABASE_FILE")
    if configured:
        return Path(configured)
    return Path(current_app.instance_path) / "canteen.db"


def get_db() -> sqlite3.Connection:
    """Return this request's connection, opening it on first use.

    The connection is cached on ``flask.g`` for the duration of the
    request and closed by ``close_db`` at teardown. Use it as a
    transaction context manager::

        with get_db() as conn:   # commits on success, rolls back on error
            conn.execute(...)
    """
    if "db" not in g:
        conn = sqlite3.connect(db_path())
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def close_db(exc=None) -> None:
    """Close the request's connection. Registered as an app teardown."""
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db() -> None:
    """Create the schema if missing and seed the sample menu once."""
    with get_db() as conn:
        conn.executescript(SCHEMA)
        count = conn.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO menu_items(name, category, price, available) "
                "VALUES (?, ?, ?, 1)",
                SEED_MENU,
            )
