from __future__ import annotations

import pytest
from src.service.nugget_wallet.nugget_wallet_service import NuggetWalletService


class TestNuggetWalletService:
    def test_add_positive_nuggets(self) -> None:
        svc = NuggetWalletService()
        result = svc.add_nuggets("wallet_1", 100.0)
        assert result == 100.0

    def test_add_negative_nuggets_raises(self) -> None:
        svc = NuggetWalletService()
        with pytest.raises(ValueError, match="Cannot add negative nuggets"):
            svc.add_nuggets("wallet_1", -10.0)

    def test_deduct_valid(self) -> None:
        svc = NuggetWalletService()
        result = svc.deduct_nuggets("wallet_1", 50.0)
        assert result is True

    def test_deduct_negative_raises(self) -> None:
        svc = NuggetWalletService()
        with pytest.raises(ValueError, match="Cannot deduct negative nuggets"):
            svc.deduct_nuggets("wallet_1", -5.0)

    def test_get_balance(self) -> None:
        svc = NuggetWalletService()
        balance = svc.get_balance("wallet_1")
        assert isinstance(balance, float)
