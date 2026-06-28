from __future__ import annotations

import pytest


def test_pin_matches() -> None:
    assert "1234" == "1234"


def test_pin_does_not_match() -> None:
    assert "1234" != "0000"
