"""Service layer (business logic).

Business rules that must be testable independently of HTTP live here:
order pricing, inventory consumption, payment handling, approvals.

The prototype currently keeps this logic inside the route handlers. As
each phase of BUILD_PLAN.md lands, move the rule into a function in this
package and have the route call it, e.g.::

    # app/services/orders.py
    def place_order(student, cart) -> Order: ...

Routes then own only parsing, authorization and rendering.
"""
