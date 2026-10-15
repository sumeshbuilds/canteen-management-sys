"""Application configuration.

Everything the app can be tuned with lives here, driven by environment
variables so the same code runs in development, testing and production
without edits. See ``.env.example`` for the variables that are read.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _sqlite_uri(path: Path) -> str:
    # SQLAlchemy needs POSIX-style separators even on Windows.
    return f"sqlite:///{path.as_posix()}"


class Config:
    """Base configuration shared by every environment."""

    # --- Core ---------------------------------------------------------
    APP_NAME = "College Canteen Management System"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # --- Database -----------------------------------------------------
    # The prototype stores data in a single SQLite file using the stdlib
    # sqlite3 driver (see app/db.py). DATABASE_FILE is the one place that
    # path is configured. Phase 1 switches to SQLAlchemy + Flask-Migrate
    # and uses SQLALCHEMY_DATABASE_URI instead.
    DATABASE_FILE = INSTANCE_DIR / "canteen.db"
    DATABASE_URL = os.environ.get("DATABASE_URL") or _sqlite_uri(DATABASE_FILE)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Business rules ----------------------------------------------
    CURRENCY_SYMBOL = "₹"
    CURRENCY_CODE = "INR"
    MAX_ORDER_QUANTITY = 50
    ITEMS_PER_PAGE = 25
    LOW_STOCK_THRESHOLD_DEFAULT = 10
    STAFF_ROLES = (
        "super_admin",
        "manager",
        "storekeeper",
        "cashier",
        "kitchen",
    )

    # --- Session / security ------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", False)
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    ENV = "testing"
    SECRET_KEY = "testing-secret"
    WTF_CSRF_ENABLED = False
    # Tests point DATABASE_FILE at a throwaway file (see tests/test_smoke.py).


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(name: str | None = None):
    """Return a config class by name, defaulting to the FLASK_ENV value."""
    name = name or os.environ.get("FLASK_ENV", "default")
    return CONFIG_MAP.get(name, DevelopmentConfig)
