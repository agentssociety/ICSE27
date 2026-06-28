from __future__ import annotations

import pytest

from src.api.urgency_level.urgency_level_router import router
from src.dto.urgency_level.urgency_level_dto import UrgencyLevelCreateRequest, UrgencyLevelUpdateRequest, UrgencyLevelResponse


def test_router_exists() -> None:
    """The urgency_level router is defined and has routes."""
    assert router is not None
    assert len(router.routes) > 0


def test_router_has_crud_routes() -> None:
    """The router has GET, POST, PUT, DELETE routes."""
    methods = set()
    for route in router.routes:
        for method in route.methods:
            methods.add(method)
    assert "GET" in methods
    assert "POST" in methods
    assert "PUT" in methods
    assert "DELETE" in methods
