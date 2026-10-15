# Migrations

Reserved for [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Alembic).

Phase 1 of `BUILD_PLAN.md` introduces Flask-Migrate and initialises this
directory with `flask db init`. Revision files are generated; do not edit
them by hand. Until then the schema is created by `app/db.py` on startup.
