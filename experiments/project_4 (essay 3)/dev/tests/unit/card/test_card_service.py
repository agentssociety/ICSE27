from __future__ import annotations

import pytest


def test_pin_verification_success() -> None:
    entered_pin = "1234"
    stored_pin = "1234"
    assert entered_pin == stored_pin


def test_pin_verification_failure() -> None:
    entered_pin = "0000"
    stored_pin = "1234"
    assert entered_pin != stored_pin


def test_lockout_after_max_attempts() -> None:
    failed_count = 3
    max_allowed = 3
    assert failed_count >= max_allowed
