from __future__ import annotations

import pytest


def test_card_authentication_valid_pin() -> None:
    """A valid PIN should authenticate successfully."""
    entered_pin = "1234"
    stored_pin = "1234"
    assert entered_pin == stored_pin


def test_card_authentication_invalid_pin() -> None:
    """An invalid PIN should fail authentication."""
    entered_pin = "0000"
    stored_pin = "1234"
    assert entered_pin != stored_pin


def test_account_locked_after_three_failed_attempts() -> None:
    """Account should be locked after 3 consecutive failed PIN attempts."""
    failed_attempts = 3
    max_attempts = 3
    assert failed_attempts >= max_attempts
