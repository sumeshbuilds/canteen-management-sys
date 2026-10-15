# COLLEGE CANTEEN MANAGEMENT SYSTEM
## B.Sc. Computer Science Project Report

### 1. Abstract
The College Canteen Management System is a web-based application designed to simplify food ordering and canteen operations in a college. Students can view available food items, select quantities, place orders, and track order status. Canteen staff can manage the menu, update order status, and view daily order and sales summaries. The system uses Python Flask for server-side processing and SQLite for data storage. It is designed as a zero-cost academic prototype.

### 2. Problem Statement
Manual canteen ordering may create queues, calculation mistakes, and difficulty maintaining records. A simple digital system can organize menu information, order details, and daily sales in one place.

### 3. Objectives
- Display food items, categories, prices, and availability.
- Allow students to submit food orders.
- Calculate order totals automatically.
- Store orders and order items in a database.
- Allow canteen staff to update order status.
- Provide a basic daily sales summary.

### 4. Scope
This version supports local demonstration on a computer. It does not include online payment, student login, inventory deduction, or secure multi-user access. Those can be future enhancements.

### 5. Hardware and Software Requirements
- Computer with Python 3.10+
- Web browser
- Python Flask
- SQLite
- HTML, CSS, JavaScript
- Visual Studio Code (optional)

### 6. System Modules
1. **Menu module:** Displays available food items and prices.
2. **Order module:** Accepts student name, roll number, and quantities.
3. **Billing module:** Calculates totals using item prices and quantities.
4. **Order tracking module:** Shows saved order details and current status.
5. **Admin module:** Adds menu items, enables/disables items, and updates order status.
6. **Sales summary module:** Calculates daily order count and sales from stored orders.

### 7. Database Design
**menu_items**
- id: Primary key
- name: Unique food item name
- category: Item category
- price: Item price
- available: Availability flag

**orders**
- id: Primary key / order number
- student_name: Student name
- student_id: Roll number or student identifier
- total: Order total
- status: Current order status
- created_at: Date and time

**order_items**
- id: Primary key
- order_id: Foreign key referencing orders
- menu_item_id: Foreign key referencing menu_items
- item_name: Snapshot of item name at order time
- quantity: Quantity ordered
- unit_price: Price at order time

### 8. System Workflow
1. Student opens the menu page.
2. Student selects one or more food items and quantities.
3. Student enters their name and roll number.
4. System validates the input and calculates the total.
5. System saves the order and its items in SQLite.
6. System displays an order number and confirmation.
7. Canteen staff open the admin dashboard and update the order status.
8. Student checks status using the order number.

### 9. Testing Plan
| Test case | Expected result |
|---|---|
| Open home page | Available menu items display |
| Submit blank student details | Validation message appears |
| Place order with no item selected | Order is rejected with a message |
| Place a valid order | Order number and total display |
| Track a valid order number | Order details and status display |
| Track an invalid order number | Not-found message displays |
| Add a valid menu item | Item appears in admin menu |
| Change an order status | Updated status is saved |
| Disable a menu item | Item is removed from student menu |
| View admin dashboard | Daily count and sales are displayed |

### 10. Advantages
- Low cost and simple to run locally
- Reduces manual bill calculation
- Maintains digital order records
- Easy to modify and extend
- Demonstrates full-stack web development and database concepts

### 11. Limitations
- No login or role-based access in the prototype
- No online payment integration
- No stock/inventory management
- Runs locally unless deployed separately
- Daily sales is a simple order-total summary, not formal accounting

### 12. Future Enhancements
- Secure admin and student login
- Inventory and stock alerts
- Menu search and filters
- Order queue display for kitchen staff
- Downloadable daily sales report
- QR-code menu
- Online payment integration using a legitimate payment provider
- Deployment to a free hosting tier, subject to provider limits and availability

### 13. Conclusion
The College Canteen Management System demonstrates how a web application can improve basic canteen operations. It combines frontend development, server-side programming, database management, form validation, and reporting in one manageable B.Sc. Computer Science project.

### 14. Viva Questions
1. What is the purpose of the project?
2. Why is Flask used?
3. What is SQLite?
4. What is the difference between frontend and backend?
5. What is a primary key?
6. Why are foreign keys used in the order tables?
7. How is the total bill calculated?
8. What is CRUD?
9. How does the application validate form input?
10. What is the purpose of the order status field?
11. Why should an admin page have authentication?
12. What improvements would you make before real-world deployment?
