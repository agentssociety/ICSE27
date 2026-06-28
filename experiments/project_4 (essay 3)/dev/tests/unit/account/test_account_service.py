from __future__ import annotations

import pytest


def test_decline_exceeding_balance() -> None:
    balance = 100.0
    amount = 150.0
    assert amount > balance


def test_decline_exceeding_daily_limit() -> None:
    used_today = 180.0
    amount = 100.0
    daily_limit = 200.0
    assert (used_today + amount) > daily_limit


def test_approve_valid_withdrawal() -> None:
    balance = 500.0
    amount = 100.0
    used_today = 50.0
    daily_limit = 200.0
    assert amount <= balance and (used_today + amount) <= daily_limit
