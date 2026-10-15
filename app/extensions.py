"""Shared Flask extension instances.

Nothing is wired up here yet: the prototype ships with Flask only, and
the forms are deliberately CSRF-exempt so the unauthenticated demo keeps
working.

Phase 1 of BUILD_PLAN.md adds the objects below and initialises them in
``app/__init__.py``::

    db = SQLAlchemy()
    migrate = Migrate()
    login_manager = LoginManager()
    csrf = CSRFProtect()

They belong in a dedicated module so that models and blueprints can
import them without creating circular imports with ``create_app``.
"""
