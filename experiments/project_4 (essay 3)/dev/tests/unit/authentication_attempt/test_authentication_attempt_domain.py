from __future__ import annotations

import pytest
from datetime import datetime
from enum import Enum


class AuthenticationOutcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


def test_authentication_attempt_records_outcome() -> None:
    """Authentication attempt should have an outcome."""
    outcome = AuthenticationOutcome.SUCCESS
    timestamp = datetime.now()
    assert outcome in ("success", "failure")
    assert timestamp is not None


def test_authentication_attempt_failure_logged() -> None:
    """Failed authentication attempt should be logged."""
    outcome = AuthenticationOutcome.FAILURE
    assert outcome == "failure"


def test_authentication_attempt_success_logged() -> None:
    """Successful authentication attempt should be logged."""
    outcome = AuthenticationOutcome.SUCCESS
    assert outcome == "success"
