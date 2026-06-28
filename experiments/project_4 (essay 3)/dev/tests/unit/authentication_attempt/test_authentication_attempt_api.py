from __future__ import annotations

import pytest


def test_list_endpoint() -> None:
    from src.api.authentication_attempt.authentication_attempt_router import router
    assert router is not None


def test_create_endpoint() -> None:
    from src.api.authentication_attempt.authentication_attempt_router import create_authentication_attempt
    assert create_authentication_attempt is not None
