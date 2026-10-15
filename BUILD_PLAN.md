# Build Plan — College Canteen Management System

Companion to [`PRD.md`](./PRD.md) (what to build) and
[`DOCUMENTATION.md`](./DOCUMENTATION.md) (how the code works today).

This file is the **roadmap**. Work is done **one phase at a time**, in
order, and each phase must be built, tested and verified before the next
one starts (PRD §10, §12).

---

## 0. How to use this plan

1. Open the phase you are working on.
2. Read its goal, deliverables, database changes and definition of done.
3. Implement it, then run the tests.
4. Record the outcome under **Phase log** at the bottom of this file
   (files changed, features, tests, limitations, next step — PRD §12).
5. Only then start the next phase.

**Working agreement**
- Real, working functionality only — no mockups or placeholder buttons
  that look complete (PRD §12.9/§12.10).
- Server-side authorization on every protected operation.
- Business rules live in services/models, never in templates (PRD §7).
- Build incrementally; never attempt the whole system in one pass.

---

## 1. Current status

| Item | State |
|---|---|
| **Phase 0 — Restructure & scaffolding** | ✅ **Done** (see §4) |
| Phase 1 — Foundation (auth, roles, ORM, migrations) | ⬜ Next |
| Phase 2 — Menu & ordering | ⬜ |
| Phase 3 — Billing & kitchen | ⬜ |
| Phase 4 — Inventory & recipes | ⬜ |
| Phase 5 — Purchasing | ⬜ |
| Phase 6 — Reporting & hardening | ⬜ |

The app currently runs as the **original demo** (anonymous menu browsing,
order placement, order tracking, unauthenticated admin), but inside the
final modular structure so every later phase has a home.

Run it:

```bash
python app.py            # http://127.0.0.1:5000
python -m unittest discover -s tests -v     # 8 smoke tests, all passing
```

---

## 2. Target structure (already in place)

```
college_canteen_management/
├── app.py                     # entry point -> create_app()
├── config.py                  # Config / Development / Testing / Production
├── requirements.txt           # Flask (runtime)
├── requirements-dev.txt       # pytest (dev)
├── .env.example               # environment variables template
├── .gitignore
├── README.md
├── PRD.md
├── PROJECT_REPORT.md
├── DOCUMENTATION.md
├── BUILD_PLAN.md              # this file
├── instance/                  # runtime data (gitignored)
│   └── canteen.db
├── migrations/                # Flask-Migrate (Phase 1)
├── app/
│   ├── __init__.py            # create_app() factory
│   ├── extensions.py          # SQLAlchemy/Migrate/Login/CSRF (Phase 1)
│   ├── db.py                  # current raw-SQL layer (Phase 1 retires it)
│   ├── models/                # SQLAlchemy models (Phase 1)
│   ├── services/              # business logic (grows each phase)
│   ├── auth/                  # Phase 1
│   ├── admin/                 # demo now, hardened in Phase 1
│   ├── manager/               # Phase 1 dashboards / Phase 6 reports
│   ├── menu/                  # ✅ demo implemented
│   ├── orders/                # ✅ demo implemented
│   ├── payments/              # Phase 3
│   ├── kitchen/               # Phase 3
│   ├── inventory/             # Phase 4
│   ├── purchasing/            # Phase 5
│   ├── reports/               # Phase 6
│   ├── templates/             # shared Jinja templates (+ errors/)
│   └── static/                # style.css
└── tests/                     # unittest now, pytest from Phase 1
```

**Blueprint registry.** `app/__init__.py` holds a `BLUEPRINTS` tuple.
Each phase imports its blueprint and appends it there.

| Blueprint | URL prefix | Module | Status |
|---|---|---|---|
| `menu` | `/` | `app/menu` | ✅ demo |
| `orders` | `/` | `app/orders` | ✅ demo |
| `admin` | `/admin` | `app/admin` | ✅ demo (no auth) |
| `auth` | `/auth` | `app/auth` | Phase 1 |
| `manager` | `/manager` | `app/manager` | Phase 1 |
| `kitchen` | `/kitchen` | `app/kitchen` | Phase 3 |
| `payments` | `/payments` | `app/payments` | Phase 3 |
| `inventory` | `/inventory` | `app/inventory` | Phase 4 |
| `purchasing` | `/purchasing` | `app/purchasing` | Phase 5 |
| `reports` | `/reports` | `app/reports` | Phase 6 |

---

## 3. Cross-cutting conventions (apply from Phase 1)

| Concern | Decision |
|---|---|
| **Money** | Store as integer minor units (paise) or `Numeric(10,2)`. Never binary float (PRD §5). |
| **Timestamps** | Store UTC; format to local time in templates (PRD §5). |
| **Authorization** | A single decorator, e.g. `@requires_roles("super_admin")`, applied to every protected route. UI hiding is never the only control (PRD §4.1). |
| **Business logic** | In `app/services/*`, called by routes; unit-tested without HTTP (PRD §9). |
| **Transactions** | Related writes (order + items, stock + movement) succeed or fail together (PRD §6.9). |
| **History** | Never hard-delete financial/inventory records; snapshot names and prices (PRD §6.11). |
| **Pagination** | All list endpoints paginate via `ITEMS_PER_PAGE` (PRD §7). |
| **Errors** | Friendly templates in `app/templates/errors/`; no secrets in responses (PRD §7). |
| **Testing** | `pytest`; each phase adds tests for its rules before it is marked done. |

---

## 4. Phase 0 — Restructure & scaffolding ✅ DONE

**Goal:** move the demo into the final modular structure without losing
working functionality.

Delivered:
- `app/` package with `create_app()` factory; `app.py` is now a thin entry point.
- `config.py` with environment-driven config classes.
- Blueprints: `menu` (`/`), `orders` (place/confirm/track), `admin` (`/admin`).
- `app/db.py` — raw SQL isolated to one module; connections now cached on
  `flask.g` and closed at teardown (fixes an unclosed-connection bug).
- `instance/canteen.db` (moved out of the source root; gitignored).
- `app/templates/`, `app/static/` moved into the package; endpoints
  updated to blueprint-qualified names (`menu.index`, `orders.place_order`, …).
- `tests/test_smoke.py` — 8 tests, passing.
- `migrations/`, `requirements-dev.txt`, `.gitignore`, `.env.example`.
- Stub packages with documented purpose for all future modules.

Verified: `python app.py` serves `/`, `/order-status`, `/admin`; 8/8 tests pass.

Known gaps carried into Phase 1: `/admin` has no authentication; no CSRF;
`secret_key` default is insecure; order lookup is enumerable; data layer is
raw SQL rather than an ORM.

---

## 5. Phase 1 — Foundation

**Goal:** one authentication system, roles/permissions, the ORM, and
role-specific dashboard shells.

### Dependencies to add
`Flask-SQLAlchemy`, `Flask-Migrate`, `Flask-Login`, `Flask-WTF`, `pytest`.

### Database (PRD §5)
New tables: `users`, `roles`, `permissions`, `user_roles`,
`role_permissions`. Introduce Alembic and generate the first migration.

### Work
1. `app/extensions.py` — create and initialise `db`, `migrate`,
   `login_manager`, `csrf`; wire them in `create_app()`.
2. `app/models/identity.py` — `User`, `Role`, `Permission` + link tables;
   hashed passwords (`werkzeug.security`).
3. Port `menu_items` / `orders` / `order_items` to models
   (`app/models/menu.py`, `app/models/orders.py`) and retire `app/db.py`.
4. `app/auth/` — login, logout, session, activation/deactivation, role
   assignment; authorization decorator in `app/auth/decorators.py`.
5. Seed roles/permissions and a Super Admin on first run.
6. `app/admin/`, `app/manager/` — dashboard shells; secure `/admin` behind
   `super_admin`.
7. Enable CSRF on all forms; move `SECRET_KEY` to the environment.
8. `app/templates/errors/` — 403, 404, 500 pages; register handlers.

### Tests
Login/logout, password hashing, role gate returns 403 for the wrong role,
deactivated user cannot log in, protected route redirects when anonymous.

### Definition of done
- Every configured role can log in and lands on the right dashboard.
- `/admin` and other protected routes reject anonymous/wrong-role access
  **server-side**.
- `flask db upgrade` builds a clean database; migrations are in `migrations/`.
- CSRF is enforced; no hardcoded secret.

---

## 6. Phase 2 — Menu & ordering

**Goal:** real menu management and a validated ordering workflow with a
proper status machine.

### Database
`menu_categories`; extend `menu_items` (description, image, category FK);
`order_status_history`; unique human-readable order number.

### Work
- Category + item CRUD with price/availability; search and filter.
- Availability enforced so unavailable items cannot be ordered.
- Price changes never alter historical `order_items`.
- Cart, quantity update, item removal, server-side pricing.
- Order status transitions (`PENDING → CONFIRMED → PREPARING → READY →
  COMPLETED`, plus `CANCELLED` / `REJECTED`) validated; each important
  transition recorded with timestamp + actor.
- Students see only their own orders (fixes the current IDOR).

### Tests
State-machine rejects invalid transitions; historical price immutability;
unavailable item rejected; student cannot read another student's order.

### Definition of done
Server-priced bills are correct, invalid transitions are rejected, and
order history is immutable.

---

## 7. Phase 3 — Billing & kitchen

**Goal:** payments (simulated), receipts, and the kitchen queue.

### Database
`payments`, `refunds`, `cashier_shifts`; order gains `payment_method`.

### Work
- Payment statuses (`PENDING/PAID/FAILED/REFUNDED/PARTIALLY_REFUNDED`)
  kept **separate** from order status (PRD §4.5, §6.8).
- Receipt generation; refund records; cashier shift totals.
- Simulated digital payment, clearly labelled as **not** a real bank
  transaction (PRD §4.5).
- Kitchen queue with items, quantities, elapsed time; `PREPARING`/`READY`
  transitions; collection recorded separately; duplicate processing blocked.

### Tests
No duplicate payments on repeat submit; refunds traceable; kitchen cannot
change finance records.

### Definition of done
Payments are independent of order status, receipts render, and the
kitchen queue drives preparation to collection.

---

## 8. Phase 4 — Inventory & recipes

**Goal:** inventory with a movement ledger, and recipe-based consumption.

### Database
`inventory_categories`, `inventory_items`, `stock_movements`,
`stock_adjustments`, `wastage_records`, `recipes`, `recipe_ingredients`
(`stock_reservations` if reservations are implemented).

### Work
- Items with SKU, base unit (g/ml/pieces), current stock, reorder threshold.
- **Every** stock change writes a `stock_movements` row in the same
  transaction (PRD §6.5, §6.9). No direct balance edits.
- Recipes link items to ingredients with per-serving quantities.
- Ingredient availability checked before accepting an order; consumption
  recorded per the documented policy; no double consumption (PRD §6.10).
- Wastage / damaged / expired records and physical-count adjustments, each
  with a reason and an actor; approvals where required.
- Low-stock detection; negative stock prevented.

### Tests
A stock change without a movement fails; goods issued reduce stock exactly
once; recipe math; low-stock threshold triggers.

### Definition of done
Inventory balances always reconcile with the movement ledger, and recipes
produce correct expected consumption.

---

## 9. Phase 5 — Purchasing

**Goal:** suppliers and the purchase-to-stock workflow.

### Database
`suppliers`, `purchase_requests`, `purchase_request_items`,
`purchase_orders`, `purchase_order_items`, `goods_receipts`,
`goods_receipt_items`.

### Work
- Supplier registration and contacts.
- Workflow: `LOW_STOCK → PURCHASE_REQUESTED → PENDING_APPROVAL →
  APPROVED/REJECTED → ORDERED → PARTIALLY_RECEIVED/RECEIVED → CLOSED`.
- A request never increases stock directly; only a **goods receipt** does,
  by the **actual received** quantity (PRD §6.6, §6.7).
- Partial deliveries supported; separation of duties enforced so a user
  cannot approve their own sensitive request (PRD §6.12).

### Tests
Approval does not change stock; partial receipt increases by received amount
only; self-approval blocked.

### Definition of done
Stock increases only via goods receipts, matching received quantities.

---

## 10. Phase 6 — Reporting & hardening

**Goal:** date-filtered reports, audit logs, tests, and a security pass.

### Database
`expenses`, `audit_logs` (and `cashier_shifts` if not already added).

### Work
- Reports: daily/monthly sales, order volume, item-wise sales, payment
  methods, cancellations, refunds, low stock, stock movements, consumption,
  wastage, purchases, supplier receipts, cashier closing (PRD §4.11).
- Clearly separate sales, purchase expenditure, consumption cost and
  estimated profit — **never** label gross sales as profit.
- CSV export for authorised reports.
- Audit logging for sensitive actions, excluding secrets (PRD §4.12).
- Security review: rate limiting, secure cookies, safe error handling.
- Full test pass; update `DOCUMENTATION.md` and README.

### Definition of done
Reports match underlying records, audit logs capture sensitive actions, and
a new developer can run and test the app from the README alone.

---

## 11. Phase log

> Append one entry per completed phase (PRD §12).

### Phase 0 — Restructure & scaffolding
- **Files created/modified:** `app.py`, `config.py`, `app/__init__.py`,
  `app/db.py`, `app/extensions.py`, `app/menu/*`, `app/orders/*`,
  `app/admin/*`, `app/models/__init__.py`, `app/services/__init__.py`,
  stub packages (`auth`, `manager`, `inventory`, `purchasing`, `payments`,
  `kitchen`, `reports`), `tests/test_smoke.py`, `.gitignore`,
  `.env.example`, `requirements-dev.txt`, `migrations/README.md`;
  templates and static moved into `app/`; database moved to `instance/`.
- **Features:** unchanged demo behaviour, now behind an app factory and
  blueprints.
- **Database changes:** none (schema unchanged); file relocated to
  `instance/canteen.db`.
- **Tests:** 8 smoke tests via `python -m unittest discover -s tests` → OK.
- **Known limitations:** `/admin` unauthenticated; no CSRF; default secret;
  enumerable order lookup; raw SQL data layer.
- **Next:** Phase 1 — Foundation.

---

## 12. Deviations from the PRD (current, intentional)

| PRD | Current | Why / when fixed |
|---|---|---|
| SQLAlchemy ORM + migrations (§2, §5) | raw `sqlite3` in `app/db.py` | Phase 0 kept the demo working; Phase 1 introduces the ORM + Alembic. |
| Flask-Login / CSRF (§2, §4.1) | not enabled | Enabling now would break the unauthenticated demo. Phase 1. |
| §9 shows both `app.py` and `app/` | same, and it works | The package shadows the script for imports; `app.py` is only ever run as `__main__`. |
| Money as decimal (§5) | `REAL` floats | Inherited from the demo; Phase 1 moves to integer minor units / `Numeric`. |
| Paginated lists (§7) | `/admin` loads last 100 orders | Phase 1/2 paginate with `ITEMS_PER_PAGE`. |
