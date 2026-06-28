"""Configuration for Blood Bank Management Application.

This module provides a centralized configuration class that is used across
all application modules. Sensitive values should be overridden via environment
variables in production.
"""

import os
from typing import Final


class Config:
    """Application configuration.

    Attributes:
        SECRET_KEY: Flask secret key for session signing.
        SQLALCHEMY_DATABASE_URI: Database connection string (SQLite by default).
        STOCK_ALERT_THRESHOLD: Minimum stock level before raising an alert.
        EXPIRATION_CHECK_INTERVAL_HOURS: How often to check and mark expired units.
        RESERVATION_RELEASE_MINUTES: Time after which unconfirmed reservations are released.
        ALERT_CHECK_INTERVAL_MINUTES: How often to check stock levels and create alerts.
    """

    # Flask security
    SECRET_KEY: Final[str] = os.environ.get(
        "BLOODBANK_SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # Database (SQLite for local development; set via env var for other DBs)
    SQLALCHEMY_DATABASE_URI: Final[str] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///bloodbank.db"
    )

    # Stock alert threshold (units)
    STOCK_ALERT_THRESHOLD: Final[int] = int(
        os.environ.get("STOCK_ALERT_THRESHOLD", "5")
    )

    # Background job intervals (in minutes / hours)
    EXPIRATION_CHECK_INTERVAL_HOURS: Final[int] = int(
        os.environ.get("EXPIRATION_CHECK_INTERVAL_HOURS", "1")
    )

    RESERVATION_RELEASE_MINUTES: Final[int] = int(
        os.environ.get("RESERVATION_RELEASE_MINUTES", "1440")  # 24 hours
    )

    ALERT_CHECK_INTERVAL_MINUTES: Final[int] = int(
        os.environ.get("ALERT_CHECK_INTERVAL_MINUTES", "5")
    )

    # Prevent arbitrary attributes
    def __setattr__(self, name, value):
        raise AttributeError("Config attributes are read-only")
