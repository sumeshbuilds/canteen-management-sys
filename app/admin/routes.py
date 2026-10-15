"""Admin routes: dashboard, menu management and order status."""
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from app.db import get_db
from app.admin import bp

# Statuses the demo workflow allows. Phase 2 replaces this with a
# validated state machine (BUILD_PLAN.md).
ORDER_STATUSES = ("Received", "Preparing", "Ready", "Completed", "Cancelled")


# Empty rule (not "/") so the URL is exactly /admin rather than /admin/.
@bp.route("", methods=["GET", "POST"])
def dashboard():
    """Manage the menu and orders, and show today's totals.

    WARNING: no authentication yet. Add login + role checks before this
    is exposed anywhere but a local machine.
    """
    if request.method == "POST":
        action = request.form.get("action")
        with get_db() as conn:
            if action == "add_item":
                _handle_add_item(conn)
            elif action == "toggle_item":
                conn.execute(
                    "UPDATE menu_items SET available=CASE available WHEN 1 THEN 0 ELSE 1 END WHERE id=?",
                    (request.form.get("item_id"),),
                )
                flash("Menu availability updated.", "success")
            elif action == "update_status":
                order_id = request.form.get("order_id")
                status = request.form.get("status")
                if status in ORDER_STATUSES:
                    conn.execute(
                        "UPDATE orders SET status=? WHERE id=?", (status, order_id)
                    )
                    flash("Order status updated.", "success")
            elif action == "delete_order":
                conn.execute(
                    "DELETE FROM orders WHERE id=?", (request.form.get("order_id"),)
                )
                flash("Order deleted.", "success")
        return redirect(url_for("admin.dashboard"))

    with get_db() as conn:
        items = conn.execute(
            "SELECT * FROM menu_items ORDER BY category, name"
        ).fetchall()
        orders = conn.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT 100"
        ).fetchall()
        today = datetime.now().strftime("%Y-%m-%d")
        # Single aggregate query for today's count and sales.
        row = conn.execute(
            "SELECT COUNT(*) AS order_count, COALESCE(SUM(total), 0) AS sales "
            "FROM orders WHERE date(created_at)=? AND status!='Cancelled'",
            (today,),
        ).fetchone()
    return render_template(
        "admin.html",
        items=items,
        orders=orders,
        sales=row["sales"],
        order_count=row["order_count"],
        order_statuses=ORDER_STATUSES,
    )


def _handle_add_item(conn) -> None:
    """Validate and insert a new menu item, flashing the outcome."""
    import sqlite3

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    try:
        price = float(request.form.get("price", ""))
        if not name or not category or price < 0:
            raise ValueError
        conn.execute(
            "INSERT INTO menu_items(name, category, price, available) VALUES (?, ?, ?, 1)",
            (name, category, price),
        )
        flash("Menu item added.", "success")
    except sqlite3.IntegrityError:
        flash("An item with that name already exists.", "error")
    except ValueError:
        flash("Enter a valid item name, category, and non-negative price.", "error")
