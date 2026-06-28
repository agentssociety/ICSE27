from __future__ import annotations

import pytest


def test_list_endpoint() -> None:
    from src.api.daily_withdrawal_limit.daily_withdrawal_limit_router import router
    assert router is not None


def test_create_endpoint() -> None:
    from src.api.daily_withdrawal_limit.daily_withdrawal_limit_router import create_daily_withdrawal_limit
    assert create_daily_withdrawal_limit is not None
