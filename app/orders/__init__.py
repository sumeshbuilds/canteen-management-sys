"""Ordering module (public).

Handles order placement, the confirmation receipt and order tracking.
Billing rules live in ``app/services`` once that layer is introduced.
"""
from flask import Blueprint

bp = Blueprint("orders", __name__)

from app.orders import routes  # noqa: E402,F401  (imported after bp on purpose)
