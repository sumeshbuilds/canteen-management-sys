"""Order routes: place, confirm and track."""
from datetime import datetime

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.db import get_db
from app.orders import bp


@bp.route("/place-order", methods=["POST"])
def place_order():
    """Validate a submitted cart and persist the order.

    The browser total is never trusted: every price is re-read from the
    database and the total is recalculated here.
    """
    student_name = request.form.get("student_name", "").strip()
    student_id = request.form.get("student_id", "").strip()
    quantities = request.form.getlist("quantity")
    item_ids = request.form.getlist("item_id")
    max_qty = current_app.config["MAX_ORDER_QUANTITY"]

    if not student_name or not student_id:
        flash("Please enter your name and student ID.", "error")
        return redirect(url_for("menu.index"))

    cart = []
    try:
        with get_db() as conn:
            for item_id, quantity in zip(item_ids, quantities):
                qty = int(quantity or 0)
                if qty < 0 or qty > max_qty:
                    raise ValueError
                if qty > 0:
                    item = conn.execute(
                        "SELECT * FROM menu_items WHERE id=? AND available=1",
                        (int(item_id),),
                    ).fetchone()
                    if item:
                        cart.append((item, qty))
            if not cart:
                flash("Choose at least one item before placing your order.", "error")
                return redirect(url_for("menu.index"))

            total = sum(float(item["price"]) * qty for item, qty in cart)
            cur = conn.execute(
                "INSERT INTO orders(student_name, student_id, total, status, created_at) "
                "VALUES (?, ?, ?, 'Received', ?)",
                (
                    student_name,
                    student_id,
                    total,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            order_id = cur.lastrowid
            for item, qty in cart:
                conn.execute(
                    "INSERT INTO order_items(order_id, menu_item_id, item_name, quantity, unit_price) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (order_id, item["id"], item["name"], qty, item["price"]),
                )
        return redirect(url_for("orders.order_confirmation", order_id=order_id))
    except (ValueError, TypeError):
        flash("Please enter valid quantities.", "error")
        return redirect(url_for("menu.index"))


@bp.route("/order/<int:order_id>")
def order_confirmation(order_id):
    """Show the receipt for a freshly placed order."""
    with get_db() as conn:
        order = conn.execute(
            "SELECT * FROM orders WHERE id=?", (order_id,)
        ).fetchone()
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id=?", (order_id,)
        ).fetchall()
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("menu.index"))
    return render_template("order.html", order=order, items=items)


@bp.route("/order-status", methods=["GET", "POST"])
def order_status():
    """Look up an order by its number.

    NOTE: order numbers are sequential, so this endpoint currently lets
    anyone enumerate orders. Phase 1 must restrict lookups to the owning
    student (see BUILD_PLAN.md, business rule 2).
    """
    order = None
    items = []
    if request.method == "POST":
        order_id = request.form.get("order_id", "").strip()
        with get_db() as conn:
            order = conn.execute(
                "SELECT * FROM orders WHERE id=?", (order_id,)
            ).fetchone()
            if order:
                items = conn.execute(
                    "SELECT * FROM order_items WHERE order_id=?", (order_id,)
                ).fetchall()
            else:
                flash("No order found with that order number.", "error")
    return render_template("status.html", order=order, items=items)
