# Product Requirements Document (PRD)
## College Canteen Management System

**Version:** 1.0  
**Product type:** Web application  
**Target environment:** Local development first, production deployment later  
**Primary objective:** Build a secure, role-based canteen management system with integrated ordering, billing, inventory, purchasing, and reporting.

---

## 1. Product Overview

Build a web-based College Canteen Management System that digitizes the daily operations of a college canteen.

The application must allow administrators to manage users and permissions, managers to supervise operations, storekeepers to manage inventory, cashiers to process payments, kitchen staff to process orders, and students to place and track orders.

The system must maintain consistent records across orders, payments, inventory, supplier purchases, and financial reports.

The application should be modular, maintainable, responsive, and suitable for future expansion.

## 2. Technology Stack

Use the following stack unless the existing repository establishes a different working stack.

- Backend: Python with Flask.
- Frontend: HTML5, CSS3, JavaScript.
- UI templating: Jinja2.
- Database: SQLite for initial development.
- Database access: SQLAlchemy ORM.
- Database migrations: Flask-Migrate/Alembic.
- Authentication: Flask-Login.
- Form and request validation: WTForms or equivalent server-side validation.
- Testing: pytest.
- Charts: Chart.js if required for dashboard visualizations.
- Dependency management: requirements.txt and a Python virtual environment.

Use a modular monolithic architecture. Do not introduce microservices, unnecessary infrastructure, or complex frontend frameworks unless explicitly justified.

Before creating files, inspect the existing repository. Preserve working code where appropriate and adapt the implementation to the current project structure.

## 3. User Roles and Permissions

Implement centralized authentication and server-side role-based access control.

### 3.1 Super Admin

The Super Admin has overall system administration authority.

Permissions:
- Create, edit, activate, and deactivate user accounts.
- Assign roles and permissions.
- Manage canteen settings and branches if multi-branch support is enabled.
- Manage menu categories, food items, and pricing.
- View all orders and payments.
- View and supervise inventory.
- Approve purchase requests and stock adjustments.
- Manage suppliers and purchasing workflows.
- View financial, sales, and inventory reports.
- Review audit logs.
- Configure application settings.

Sensitive actions must be logged. Do not permit silent deletion of financial or inventory history.

### 3.2 Canteen Manager

Permissions:
- View the operational dashboard.
- Manage menu availability.
- Review orders and sales.
- Review inventory levels.
- Create or approve purchase requests according to assigned permissions.
- Review goods receipts.
- Approve permitted stock adjustments.
- Review wastage and expiry reports.
- Review cashier shift-closing reports.
- View operational reports.

The Manager must not automatically receive Super Admin privileges.

### 3.3 Inventory Manager / Storekeeper

Permissions:
- View inventory items and quantities.
- Register stock receipts.
- Record supplier deliveries.
- View stock movement history.
- Record wastage and damaged stock.
- Record batch numbers and expiry dates.
- Create purchase requisitions.
- Generate low-stock reports.
- Request stock adjustments.

The storekeeper must not directly edit stock quantities without generating an appropriate stock movement or adjustment record.

### 3.4 Cashier

Permissions:
- View orders assigned to the cashier or permitted counter.
- Process eligible payments.
- Generate receipts.
- View payment history within the assigned scope.
- Record eligible refunds subject to approval.
- View assigned shift totals.
- Record cash reconciliation at shift closing.

The cashier must not modify inventory, change menu prices without permission, or delete completed financial transactions.

### 3.5 Kitchen Staff

Permissions:
- View accepted orders in the kitchen queue.
- View order items and quantities.
- Mark orders as preparing.
- Mark orders as ready.
- View order preparation details.
- Report unavailable food items.

Kitchen staff must not access user administration, unrestricted payment records, or financial reports.

### 3.6 Student / Customer

Permissions:
- Browse published menu items.
- View item prices and availability.
- Add items to a cart.
- Place orders.
- View their own orders and receipts.
- Track order status.
- Cancel eligible orders according to policy.
- View their own payment status and order history.

Students must never access another student's private order or payment records.

## 4. Functional Requirements

### 4.1 Authentication and User Management

Implement:
- Login and logout.
- Secure password hashing.
- Account activation and deactivation.
- Role assignment.
- Authorization checks on protected routes and service operations.
- Session management.
- Appropriate unauthorized-access and forbidden-access responses.

Create one authentication system for all roles.

Redirect authenticated users to appropriate dashboards based on their permissions.

Do not rely on hiding interface elements as the only security mechanism.

### 4.2 Dashboard

Create a role-specific dashboard.

Super Admin dashboard:
- Today's sales.
- Total orders.
- Pending orders.
- Completed orders.
- Low-stock alerts.
- Pending purchase requests.
- Recent operational activities.

Manager dashboard:
- Current orders.
- Sales summary.
- Inventory alerts.
- Pending approvals.
- Wastage summary.

Storekeeper dashboard:
- Current stock.
- Low-stock items.
- Expiring inventory.
- Recent receipts.
- Pending purchase requests.

Cashier dashboard:
- Orders awaiting payment.
- Completed payments.
- Payment-method totals.
- Current shift summary.

Kitchen dashboard:
- New orders.
- Orders preparing.
- Orders ready for collection.

Student dashboard:
- Current orders.
- Recent orders.
- Order status.
- Available menu items.

Display metrics only when the current user has permission to access the underlying information.

### 4.3 Menu Management

Implement:
- Food categories.
- Food items.
- Item names and descriptions.
- Selling prices.
- Optional images.
- Availability status.
- Preparation-related metadata where necessary.
- Menu search and filtering.

Only authorized users may create or update menu items.

Unavailable items must not be orderable.

Price changes must not modify historical order prices.

### 4.4 Order Management

Students must be able to:
1. Browse the menu.
2. Add items to a cart.
3. Update quantities.
4. Remove items.
5. Review the order total.
6. Select an available payment method.
7. Submit the order.
8. View confirmation and order status.

The server must validate all item IDs, prices, quantities, availability, and ownership.

Never trust a total or unit price submitted by the browser.

Each order must have a unique, human-readable order number.

Recommended order statuses:
- PENDING
- CONFIRMED
- PREPARING
- READY
- COMPLETED
- CANCELLED
- REJECTED

Enforce valid status transitions. Record the timestamp and actor for important transitions.

Cancelled orders must not silently erase their order items or financial history.

### 4.5 Billing and Payments

Implement:
- Server-side order total calculation.
- Order item price snapshots.
- Subtotals.
- Discounts where authorized.
- Tax calculation where applicable.
- Total payable.
- Payment method.
- Payment status.
- Payment transaction reference.
- Receipt generation.
- Refund records.
- Payment history.

Supported initial payment methods:
- Cash.
- Simulated digital payment for development and demonstration.

Do not claim that a simulated payment is a real bank or payment-provider transaction.

Recommended payment statuses:
- PENDING
- PAID
- FAILED
- REFUNDED
- PARTIALLY_REFUNDED

Keep order status separate from payment status.

A real payment gateway is outside the initial scope. Integrate one only when provider credentials and the necessary configuration are available.

### 4.6 Kitchen Order Processing

Implement a kitchen queue with:
- Order number.
- Order creation time.
- Food items.
- Quantities.
- Special instructions where applicable.
- Current status.
- Time elapsed since order creation.

Kitchen staff may transition accepted orders to PREPARING and then READY.

Collection or completion should be recorded separately from preparation.

Prevent unauthorized status changes and duplicate processing.

### 4.7 Inventory Management

Support raw ingredients and directly sold finished goods.

Each inventory item should have:
- Name.
- SKU or unique code.
- Category.
- Unit of measurement.
- Current stock.
- Reorder threshold.
- Optional preferred supplier.
- Optional batch and expiry tracking.
- Active status.

Support units such as:
- Kilograms.
- Grams.
- Litres.
- Millilitres.
- Pieces.
- Packets.

Use consistent base units for calculations. For example, store ingredient quantities in grams or millilitres where appropriate.

Implement:
- Stock receipts.
- Stock issues.
- Recipe-based ingredient consumption.
- Stock reservations if needed.
- Wastage.
- Damaged goods.
- Stock adjustments.
- Low-stock alerts.
- Stock movement history.
- Physical stock reconciliation.

Never allow a stock update to occur without a corresponding traceable transaction.

Use database transactions so stock changes and stock movement records succeed or fail together.

Prevent negative stock unless an explicitly authorized workflow allows it.

### 4.8 Recipe Management

Implement recipes linking menu items to inventory ingredients.

Each recipe ingredient must specify:
- Inventory item.
- Quantity required per serving.
- Unit of measurement.

For example:

Vegetable sandwich:
- Bread: 2 slices.
- Potato: 50 g.
- Butter: 10 g.

Calculate expected ingredient consumption from the ordered or prepared quantity.

Use a clearly defined inventory policy:
- Check ingredient availability before accepting an order.
- Reserve stock when appropriate.
- Record ingredient consumption according to the chosen preparation workflow.
- Release reservations when eligible orders are cancelled.
- Prevent double consumption when an order is processed more than once.

For the initial version, use a documented and consistent consumption policy rather than implementing a complicated production-planning system.

### 4.9 Supplier and Purchase Management

Implement:
- Supplier registration.
- Supplier contact details.
- Purchase requisitions.
- Purchase approval.
- Purchase orders.
- Goods receipts.
- Supplier invoice references.
- Purchase status tracking.

Recommended purchasing workflow:

LOW_STOCK
→ PURCHASE_REQUESTED
→ PENDING_APPROVAL
→ APPROVED or REJECTED
→ ORDERED
→ PARTIALLY_RECEIVED or RECEIVED
→ CLOSED

A purchase request must not directly increase stock.

Inventory must increase only when an authorized user records a goods receipt.

The actual quantity received must determine the inventory increase, not merely the quantity ordered.

Allow partial deliveries.

### 4.10 Wastage and Stock Adjustments

Implement:
- Wastage records.
- Damaged goods records.
- Expired stock records.
- Physical count adjustments.
- Adjustment reason.
- User who recorded the event.
- Approval status when required.
- Corresponding stock movement.

Never permit an ordinary user to overwrite the inventory balance without recording why the stock changed.

### 4.11 Reports and Analytics

Implement date-filtered reports for:
- Daily and monthly sales.
- Order volume.
- Item-wise sales.
- Payment methods.
- Cancelled orders.
- Refunds.
- Low-stock inventory.
- Stock movement history.
- Ingredient consumption.
- Wastage.
- Purchase history.
- Supplier receipts.
- Cashier shift closing.

Clearly distinguish sales, purchase expenditure, ingredient consumption cost, and estimated operating profit.

Do not label gross sales as profit.

Reports must respect user permissions and date filters.

CSV export is desirable for authorized administrative reports.

### 4.12 Audit Logging

Record significant actions such as:
- User creation and deactivation.
- Role changes.
- Menu price changes.
- Purchase approvals.
- Stock adjustments.
- Inventory receipts.
- Refunds.
- Order cancellations.
- Permission changes.

Each audit entry should include:
- Actor user ID.
- Action.
- Entity type.
- Entity ID.
- Timestamp.
- Relevant before-and-after values where appropriate.
- Reason or reference when required.

Do not store passwords, session secrets, or payment credentials in audit logs.

## 5. Database Design

Use SQLAlchemy models and explicit foreign-key relationships.

Create the following core tables.

### Identity and access control
- users
- roles
- permissions
- user_roles
- role_permissions

### Menu
- menu_categories
- menu_items

### Orders
- orders
- order_items
- order_status_history

### Payments
- payments
- refunds

### Inventory
- inventory_categories
- inventory_items
- stock_movements
- stock_reservations, if reservations are implemented
- stock_adjustments
- wastage_records

### Recipes
- recipes
- recipe_ingredients

### Purchasing
- suppliers
- purchase_requests
- purchase_request_items
- purchase_orders
- purchase_order_items
- goods_receipts
- goods_receipt_items

### Finance and auditing
- expenses
- cashier_shifts
- audit_logs

Use integer primary keys or UUIDs consistently.

Use foreign keys, uniqueness constraints, non-null constraints, and indexes where appropriate.

Use decimal-safe numeric representations for monetary values. Avoid binary floating-point arithmetic for money.

Store timestamps consistently, preferably in UTC, and format them in the configured local timezone in the interface.

Store historical item names and unit prices in order items so old receipts remain accurate after menu changes.

Use database migrations rather than manually recreating tables on every application startup.

## 6. Business Rules and Data Integrity

The following rules are mandatory:

1. All protected operations require server-side authorization.
2. A student can access only their own orders and payments.
3. Order totals are calculated on the server.
4. Historical order prices remain unchanged.
5. Stock changes must create stock movement records.
6. Goods receipts increase inventory only by the actual received quantity.
7. Purchase approval does not itself increase stock.
8. Order status and payment status are separate.
9. Stock and related ledger updates must be transactional.
10. Duplicate requests must not result in duplicate payments or stock consumption.
11. Cancelled or refunded transactions must remain traceable.
12. Users must not be able to approve their own sensitive requests where separation of duties is required.
13. Unauthorized users must not be able to bypass restrictions by calling API endpoints directly.
14. Invalid state transitions must be rejected.
15. Every inventory adjustment must have a reason and an identifiable actor.

## 7. Non-Functional Requirements

### Security
- Secure password hashing.
- Role-based authorization.
- CSRF protection for session-authenticated forms.
- Input validation and output escaping.
- Secure session-cookie settings.
- Protection against SQL injection.
- Safe error handling without exposing secrets.
- Environment-based configuration for sensitive settings.

### Performance
- Paginate long order and inventory lists.
- Add indexes to frequently queried fields.
- Avoid loading entire order histories unnecessarily.
- Use efficient queries for dashboards.

### Reliability
- Use database transactions for related writes.
- Provide database backup instructions.
- Support migrations.
- Prevent inconsistent inventory balances.
- Handle failed payment and order operations safely.

### Usability
- Responsive layout for desktop, tablet, and mobile.
- Clear role-specific navigation.
- Accessible forms and labels.
- Search, filtering, and pagination.
- Clear loading, success, and error states.
- Confirmation for sensitive actions.

### Maintainability
- Separate routes, services, models, forms, templates, and configuration.
- Keep business rules out of templates.
- Reuse shared UI components.
- Add automated tests for critical workflows.
- Document setup and database initialization.

## 8. UI and Design Requirements

Create a clean, professional college canteen dashboard.

Design principles:
- Responsive sidebar navigation for administrative dashboards.
- Compact top navigation with current user and role.
- Dashboard summary cards.
- Clear tables with search and filters.
- Consistent spacing, typography, and button styles.
- Accessible color contrast.
- Clear visual indicators for order and payment statuses.
- Mobile-friendly student menu and cart.
- Kitchen-friendly order cards with prominent status actions.

Use a consistent design system rather than creating unrelated layouts for each page.

Do not sacrifice functionality or readability for decorative animations.

## 9. Application Structure

Use a modular Flask project structure similar to:

canteen_management/
- app.py
- config.py
- requirements.txt
- README.md
- instance/
- migrations/
- app/
  - __init__.py
  - extensions.py
  - models/
  - auth/
  - admin/
  - manager/
  - inventory/
  - purchasing/
  - menu/
  - orders/
  - payments/
  - kitchen/
  - reports/
  - templates/
  - static/
- tests/

Use Flask Blueprints to organize application modules.

Keep database models separate from route handlers.

Implement core business operations in service functions so that inventory consumption, order processing, and payment handling can be tested independently of the UI.

## 10. Development Phases

### Phase 1: Foundation
- Inspect repository.
- Set up Flask application.
- Configure database.
- Implement authentication.
- Implement roles and permissions.
- Create role-specific dashboard shells.

### Phase 2: Menu and Ordering
- Menu categories.
- Food item management.
- Student menu.
- Shopping cart.
- Order creation.
- Order status transitions.

### Phase 3: Billing and Kitchen
- Payment records.
- Simulated payment workflow.
- Receipt generation.
- Kitchen queue.
- Preparation and collection states.

### Phase 4: Inventory and Recipes
- Inventory items.
- Stock movement ledger.
- Recipe management.
- Ingredient availability.
- Ingredient consumption.
- Wastage and adjustments.
- Low-stock alerts.

### Phase 5: Purchasing
- Supplier management.
- Purchase requests.
- Approval workflow.
- Purchase orders.
- Partial and complete goods receipts.

### Phase 6: Reporting and Hardening
- Sales reports.
- Inventory reports.
- Cashier closing.
- Audit logs.
- Automated tests.
- Security review.
- Setup documentation.

Implement and verify each phase before proceeding to the next.

## 11. Acceptance Criteria

The application is considered functionally complete when:

- All configured roles can log in.
- Users cannot access unauthorized routes or records.
- The Super Admin can manage users and roles.
- Authorized users can manage the menu.
- Students can place and track orders.
- Server-side pricing produces correct bills.
- Kitchen staff can process valid orders.
- Payment records remain separate from order statuses.
- Inventory receipts and issues produce stock movement entries.
- Recipes calculate expected ingredient consumption correctly.
- Duplicate order-processing requests do not consume stock twice.
- Purchase requests follow the approval workflow.
- Goods receipts update stock using actual received quantities.
- Wastage and stock adjustments are traceable.
- Sales and inventory reports match the underlying records.
- Historical receipts remain accurate after menu price changes.
- Database migrations work on a clean database.
- Automated tests cover authentication, authorization, ordering, payments, and inventory.
- Setup instructions allow a new developer to run the application locally.

## 12. Instructions for OpenCode

Act as a senior full-stack engineer.

Before implementation:
1. Inspect the repository structure and existing code.
2. Identify the current stack, entry points, dependencies, and existing database models.
3. Create a concise implementation plan.
4. Identify missing requirements or conflicts with the current project.
5. Avoid overwriting functional code unnecessarily.

During implementation:
1. Build incrementally in the phases described above.
2. Create real, working application functionality rather than static mockups.
3. Implement server-side authorization for every protected operation.
4. Use database migrations and transactional service functions.
5. Add automated tests for critical business rules.
6. Run the tests and fix regressions before moving to the next phase.
7. Keep dependencies minimal.
8. Do not fabricate successful payment transactions.
9. Do not use placeholder buttons for features represented as complete.
10. Do not claim a feature is complete unless its core workflow has been implemented and verified.

At the end of each phase, report:
- Files created or modified.
- Features implemented.
- Database changes.
- Tests executed and their results.
- Known limitations.
- Next implementation steps.

Begin with repository inspection and Phase 1. Do not attempt to implement the entire system in one unverified code-generation pass.

## 13. Out of Scope for Version 1

Unless explicitly requested, do not implement:
- Real payment-gateway integration.
- Payroll management.
- Full accounting and tax filing.
- Complex multi-branch financial consolidation.
- Supplier marketplace integration.
- AI-based demand forecasting.
- Native Android or iOS applications.
- Microservices or Kubernetes deployment.

Design the application so these capabilities can be added later without requiring a complete rewrite.
