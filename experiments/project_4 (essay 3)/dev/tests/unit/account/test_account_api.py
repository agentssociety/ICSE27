from __future__ import annotations

import pytest


def test_list_endpoint() -> None:
    from src.api.account.account_router import router
    assert router is not None


def test_create_endpoint() -> None:
    from src.api.account.account_router import create_account
    assert create_account is not None
