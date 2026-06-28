from __future__ import annotations

import pytest

from src.api.dashboard.dashboard_router import router


class TestDashboardAPI:
    """Tests for Dashboard API layer."""

    def test_router_exists(self) -> None:
        assert router is not None
        assert len(router.routes) >= 1
