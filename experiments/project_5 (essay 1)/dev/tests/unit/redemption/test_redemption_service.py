from __future__ import annotations

import pytest
from src.service.redemption.redemption_service import RedemptionService


class TestRedemptionService:
    def test_check_permission(self) -> None:
        svc = RedemptionService()
        assert svc.checkPermission(None, None) is True

    def test_validate_sufficient_balance_enough(self) -> None:
        svc = RedemptionService()
        assert svc.validateSufficientBalance(100.0, 50.0) is True

    def test_validate_sufficient_balance_exact(self) -> None:
        svc = RedemptionService()
        assert svc.validateSufficientBalance(50.0, 50.0) is True

    def test_validate_sufficient_balance_not_enough(self) -> None:
        svc = RedemptionService()
        assert svc.validateSufficientBalance(30.0, 50.0) is False

    def test_execute_redemption(self) -> None:
        svc = RedemptionService()
        svc.executeRedemption(None, None, None)  # Should not raise

    def test_validate_preconditions(self) -> None:
        svc = RedemptionService()
        assert svc.validatePreconditions(None, None) is True
