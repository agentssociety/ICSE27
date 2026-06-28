from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api.withdrawal_transaction.withdrawal_transaction_router import router
from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalCreateRequest, WithdrawalResponse


class TestWithdrawalTransactionAPI:

    def test_router_exists(self) -> None:
        """Test that the router is properly instantiated."""
        assert router is not None
        assert len(router.routes) > 0

    def test_create_endpoint_exists(self) -> None:
        """Test that the create endpoint is registered."""
        from src.api.withdrawal_transaction.withdrawal_transaction_router import create_withdrawal_transaction
        assert create_withdrawal_transaction is not None

    def test_list_endpoint_exists(self) -> None:
        """Test that the list endpoint is registered."""
        from src.api.withdrawal_transaction.withdrawal_transaction_router import list_withdrawal_transactions
        assert list_withdrawal_transactions is not None

    def test_get_endpoint_exists(self) -> None:
        """Test that the get endpoint is registered."""
        from src.api.withdrawal_transaction.withdrawal_transaction_router import get_withdrawal_transaction
        assert get_withdrawal_transaction is not None

    def test_create_validates_positive_amount(self) -> None:
        """Test validation: amount must be > 0."""
        with pytest.raises(ValueError, match='must be greater than 0'):
            WithdrawalCreateRequest(account_id='acc-001', amount=-100)
