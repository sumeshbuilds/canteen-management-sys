"""Administration module.

Currently an unauthenticated demo dashboard. Phase 1 puts real
role-based access control in front of every route here (see
BUILD_PLAN.md); until then it is intentionally kept out of the public
deployment path.
"""
from flask import Blueprint

bp = Blueprint("admin", __name__, url_prefix="/admin")

from app.admin import routes  # noqa: E402,F401  (imported after bp on purpose)
