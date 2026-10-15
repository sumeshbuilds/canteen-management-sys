"""Menu browsing module (public).

Owns the student-facing menu. Order placement belongs to ``app.orders``
and menu administration to ``app.admin``.
"""
from flask import Blueprint

bp = Blueprint("menu", __name__)

from app.menu import routes  # noqa: E402,F401  (imported after bp on purpose)
