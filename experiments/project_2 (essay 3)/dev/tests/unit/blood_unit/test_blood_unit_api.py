from __future__ import annotations

import pytest


class TestBloodUnitAPI:
    def test_router_imports(self) -> None:
        """Verify the router module can be imported without errors."""
        from src.api.blood_unit.blood_unit_router import router
        assert router is not None
        assert len(router.routes) > 0
