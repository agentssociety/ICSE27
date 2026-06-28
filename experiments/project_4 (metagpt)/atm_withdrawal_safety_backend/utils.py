"""
Utility functions for the ATM Withdrawal System.

This module provides helper functions for JWT token creation/validation,
PIN hashing and verification, date/time parsing, and request validation.
All functions are designed to work within Flask application context.
"""

import decimal
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

import dateutil.parser
import dateutil.tz
from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity

# Use the bcrypt instance created in models.py to avoid duplication.
from models import bcrypt


def create_jwt_token(
    identity: Union[str, int],
    additional_claims: Optional[dict] = None
) -> str:
    """
    Create a JWT access token for a given identity (e.g., user ID).

    Args:
        identity: The identity to encode in the token (usually user ID).
        additional_claims: Optional extra claims to include.

    Returns:
        A signed JWT token string.
    """
    return create_access_token(
        identity=identity,
        additional_claims=additional_claims or {}
    )


def get_current_user_id() -> int:
    """
    Retrieve the user ID from the current JWT token.

    Requires a valid JWT token in the request header.
    Should be used within a Flask endpoint protected by @jwt_required().

    Returns:
        The user ID (int) stored in the token.

    Raises:
        RuntimeError: If called outside a request context or with invalid token.
    """
    identity = get_jwt_identity()
    if identity is None:
        raise RuntimeError("No valid JWT identity found in current request.")
    return int(identity)


def hash_pin(pin: str) -> str:
    """
    Hash a PIN using bcrypt.

    Args:
        pin: Plain-text PIN string.

    Returns:
        Bcrypt hash string.
    """
    return bcrypt.generate_password_hash(pin).decode('utf-8')


def verify_pin(pin: str, hashed: str) -> bool:
    """
    Verify a plain-text PIN against a bcrypt hash.

    Args:
        pin: Plain-text PIN string.
        hashed: Stored bcrypt hash.

    Returns:
        True if PIN matches the hash, False otherwise.
    """
    return bcrypt.check_password_hash(hashed, pin)


def parse_iso_datetime(datetime_str: str) -> datetime:
    """
    Parse an ISO 8601 date/time string into a datetime object.

    Args:
        datetime_str: String in ISO 8601 format (e.g., '2025-04-01T14:30:00Z').

    Returns:
        A timezone-aware datetime object (UTC assumed if no timezone).

    Raises:
        ValueError: If the string cannot be parsed.
    """
    dt = dateutil.parser.isoparse(datetime_str)
    if dt.tzinfo is None:
        # Assume UTC if no timezone is specified
        dt = dt.replace(tzinfo=dateutil.tz.tzutc())
    return dt


def validate_positive_decimal(value: Union[str, float, int, Decimal]) -> Decimal:
    """
    Validate and convert a value to a positive Decimal (for monetary amounts).

    Args:
        value: Input value that can be converted to Decimal.

    Returns:
        Decimal object representing the value.

    Raises:
        ValueError: If value is negative, zero, or cannot be converted.
        TypeError: If input type is not supported.
    """
    try:
        amount = Decimal(str(value))
    except (ValueError, TypeError, decimal.InvalidOperation):
        raise ValueError("Amount must be a valid decimal number.")

    if amount <= 0:
        raise ValueError("Amount must be a positive number.")

    # Ensure not more than two decimal places (optional, but good for finance)
    if amount.as_tuple().exponent < -2:
        raise ValueError("Amount cannot have more than two decimal places.")

    return amount


def get_fraud_threshold(key: str, default=None):
    """
    Retrieve a fraud detection threshold from the application configuration.

    Args:
        key: Key in the FRAUD_THRESHOLDS dictionary.
        default: Fallback value if key is not found.

    Returns:
        The threshold value, or the default if key is missing.
    """
    thresholds = current_app.config.get('FRAUD_THRESHOLDS', {})
    return thresholds.get(key, default)
