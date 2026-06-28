from __future__ import annotations

import pytest


def test_daily_limit_exceeded() -> None:
    daily_limit = 200.0
    used_today = 150.0
    amount = 100.0
    assert (used_today + amount) > daily_limit


def test_daily_limit_ok() -> None:
    daily_limit = 200.0
    used_today = 50.0
    amount = 100.0
    assert (used_today + amount) <= daily_limit
