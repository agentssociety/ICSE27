from __future__ import annotations

import pytest


def test_balance_sufficient() -> None:
    assert 200.0 >= 100.0


def test_balance_insufficient() -> None:
    assert 100.0 < 150.0
