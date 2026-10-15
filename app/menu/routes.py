"""Menu routes."""
from flask import render_template

from app.db import get_db
from app.menu import bp


@bp.route("/")
def index():
    """Show the menu of items that are currently available."""
    with get_db() as conn:
        items = conn.execute(
            "SELECT * FROM menu_items WHERE available=1 ORDER BY category, name"
        ).fetchall()
    return render_template("index.html", items=items)
