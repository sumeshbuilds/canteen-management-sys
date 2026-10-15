# College Canteen Management System

A zero-cost Flask + SQLite web application for college canteen ordering and
management. Built as a B.Sc. Computer Science project, restructured into a
modular layout so the full system in [`PRD.md`](./PRD.md) can be built in
stages.

## Features (current demo)

- Student-facing food menu with categories, prices and availability
- Order form with automatic bill calculation
- Order confirmation with a human-readable order number
- Order tracking by order number
- Admin menu management (add items, enable/disable items)
- Admin order management (Received, Preparing, Ready, Completed, Cancelled)
- Daily order count and sales total
- SQLite database created automatically with sample menu items

## Project structure

```
app.py                  # entry point -> create_app()
config.py               # environment-driven configuration
instance/canteen.db     # SQLite database (created on first run, gitignored)
app/                    # the application package
  __init__.py           #   application factory + blueprint registry
  db.py                 #   data access (raw SQL; replaced by the ORM in Phase 1)
  models/ services/     #   placeholders for the ORM and business rules
  menu/ orders/ admin/  #   implemented blueprints
  auth/ inventory/ ...  #   scaffolding for later phases
  templates/ static/    #   Jinja templates and CSS
tests/                  # smoke tests
migrations/             # Flask-Migrate home (Phase 1)
```

See [`DOCUMENTATION.md`](./DOCUMENTATION.md) for architecture and efficiency
analysis, [`BUILD_PLAN.md`](./BUILD_PLAN.md) for the phased roadmap, and
[`PRD.md`](./PRD.md) for the full requirements.

## Requirements

- Python 3.10 or newer
- A web browser
- Internet is not required to run the app after Flask is installed; Google
  Fonts are optional styling.

## Run on Windows

1. Create a virtual environment (recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Install the dependency:
   ```powershell
   pip install -r requirements.txt
   ```
3. Start the application:
   ```powershell
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.
5. Admin dashboard: `http://127.0.0.1:5000/admin`

## Run on Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Tests

The smoke tests use the standard library, so they run with no extra installs:

```bash
python -m unittest discover -s tests -v
```

They are also pytest-compatible:

```bash
pip install -r requirements-dev.txt
pytest
```

## Database

The database lives at `instance/canteen.db` and is created automatically the
first time the application starts, with sample menu items. It contains the
`menu_items`, `orders` and `order_items` tables. The `instance/` folder is
gitignored; delete the database file to reset to a fresh seeded state.

## Configuration

Copy `.env.example` to `.env` and adjust `SECRET_KEY`, `FLASK_DEBUG` and
`DATABASE_URL` as needed. Configuration classes live in `config.py`
(Development / Testing / Production).

## Important academic/demo note

This is a learning prototype. The admin page has **no login** and is not safe
for public deployment as-is. Before real use, add authentication,
authorization, CSRF protection, input validation, backups, and secure
production settings. The demo records orders but does not process online
payments. The build plan above tracks exactly which of these each phase adds.
