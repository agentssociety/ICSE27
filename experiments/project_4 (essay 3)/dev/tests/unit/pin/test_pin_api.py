from __future__ import annotations

import pytest


def test_auth_endpoint_exists() -> None:
    from src.api.pin.pin_router import router
    assert router is not None
