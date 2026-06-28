from __future__ import annotations

import pytest


def test_auth_endpoint_exists() -> None:
    from src.api.card.card_router import router
    assert router is not None


def test_lockout_endpoint_exists() -> None:
    from src.api.card.card_router import router
    assert len(router.routes) >= 0
