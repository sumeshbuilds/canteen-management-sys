"""Application factory for the College Canteen Management System.

``create_app`` is the single composition root: it builds the Flask app,
loads configuration, registers blueprints and prepares the database.

Blueprints are registered through ``BLUEPRINTS`` below. As each module in
BUILD_PLAN.md ships, import its blueprint and append it to the tuple.
"""
from pathlib import Path

from flask import Flask, render_template

from config import Config
from app.admin import bp as admin_bp
from app.db import close_db, init_db
from app.menu import bp as menu_bp
from app.orders import bp as orders_bp

# Registered blueprints. Future modules (auth, manager, inventory,
# purchasing, payments, kitchen, reports) are added here as they ship.
BLUEPRINTS = (
    menu_bp,
    orders_bp,
    admin_bp,
)


def create_app(config_object=Config) -> Flask:
    """Build and return a configured Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # The instance folder holds runtime data (the SQLite database) and is
    # never committed. It must exist before the database is opened.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    # Release each request's database connection at teardown.
    app.teardown_appcontext(close_db)

    register_error_handlers(app)

    with app.app_context():
        init_db()

    return app


def register_error_handlers(app: Flask) -> None:
    """Register friendly error pages.

    Templates for these live in ``app/templates/errors/``. They are added
    as the UI matures; until then the default Flask pages are used.
    """
    # Phase 1 adds 403/404/500 handlers backed by templates/errors/*.html.
    return None
