from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from src.service.transaction.transaction_service import (
    TransactionServiceImpl,
    WithdrawalRequest,
    WithdrawalResponse,
    TransactionResponse,
    AdminReviewRequest,
    AdminReviewAction,
    AdminReviewResponse,
)


class TestTransactionService:
    def setup_method(self) -> None:
        self._mock_txn_repo = MagicMock()
        self._mock_account_repo = MagicMock()
        self._service = TransactionServiceImpl(
            transaction_repo=self._mock_txn_repo,
            account_repo=self._mock_account_repo,
        )

    def test_successful_withdrawal(self) -> None:
        # Arrange
        account = MagicMock()
        account.id = 1
        account.balance = 100.0
        account.daily_withdrawal_limit = 1000.0
        account.withdrawn_today = 0.0
        account.user_id = 1
        account.failedAttempts = 0

        self._mock_account_repo.get_by_id.return_value = account
        self._mock_account_repo.update.return_value = account
        created_txn = MagicMock()
        created_txn.id = 42
        self._mock_txn_repo.create.return_value = created_txn

        request = WithdrawalRequest(account_id=1, amount=50.0)

        # Act
        result = self._service.withdraw(request)

        # Assert
        assert result.success is True
        assert result.transaction_id == "42"
        assert "successful" in result.message.lower()
        self._mock_account_repo.update.assert_called_once()
        self._mock_txn_repo.create.assert_called_once()

    def test_withdrawal_insufficient_balance(self) -> None:
        account = MagicMock()
        account.id = 1
        account.balance = 30.0
        account.daily_withdrawal_limit = 1000.0
        account.withdrawn_today = 0.0
        account.user_id = 1

        self._mock_account_repo.get_by_id.return_value = account

        request = WithdrawalRequest(account_id=1, amount=50.0)

        result = self._service.withdraw(request)

        assert result.success is False
        assert "insufficient" in result.message.lower()
        self._mock_account_repo.update.assert_not_called()
        self._mock_txn_repo.create.assert_not_called()

    def test_withdrawal_account_not_found(self) -> None:
        self._mock_account_repo.get_by_id.return_value = None

        request = WithdrawalRequest(account_id=999, amount=50.0)

        result = self._service.withdraw(request)

        assert result.success is False
        assert "not found" in result.message.lower()
        self._mock_account_repo.update.assert_not_called()
        self._mock_txn_repo.create.assert_not_called()

    def test_withdrawal_daily_limit_exceeded(self) -> None:
        account = MagicMock()
        account.id = 1
        account.balance = 200.0
        account.daily_withdrawal_limit = 100.0
        account.withdrawn_today = 80.0
        account.user_id = 1

        self._mock_account_repo.get_by_id.return_value = account

        request = WithdrawalRequest(account_id=1, amount=50.0)

        result = self._service.withdraw(request)

        assert result.success is False
        assert "daily" in result.message.lower() or "limit" in result.message.lower()
        self._mock_account_repo.update.assert_not_called()
        self._mock_txn_repo.create.assert_not_called()

    def test_update_failure_rolls_back(self) -> None:
        account = MagicMock()
        account.id = 1
        account.balance = 100.0
        account.daily_withdrawal_limit = 1000.0
        account.withdrawn_today = 0.0
        account.user_id = 1

        self._mock_account_repo.get_by_id.return_value = account
        self._mock_account_repo.update.return_value = None  # Simulate update failure

        request = WithdrawalRequest(account_id=1, amount=50.0)

        result = self._service.withdraw(request)

        assert result.success is False
        assert "failed" in result.message.lower()
        self._mock_account_repo.update.assert_called_once()
        self._mock_txn_repo.create.assert_not_called()

    def test_atomicity_on_exception(self) -> None:
        account = MagicMock()
        account.id = 1
        account.balance = 100.0
        account.daily_withdrawal_limit = 1000.0
        account.withdrawn_today = 0.0
        account.user_id = 1

        self._mock_account_repo.get_by_id.return_value = account
        self._mock_account_repo.update.side_effect = RuntimeError("Database connection lost")

        request = WithdrawalRequest(account_id=1, amount=50.0)

        result = self._service.withdraw(request)

        assert result.success is False
        self._mock_account_repo.update.assert_called_once()
        self._mock_txn_repo.create.assert_not_called()

    def test_get_transactions_by_user_id_returns_list(self) -> None:
        expected_txns = [MagicMock(), MagicMock()]
        self._mock_txn_repo.get_by_user_id.return_value = expected_txns

        result = self._service.get_transactions_by_user_id(user_id=42)

        assert result == expected_txns
        assert len(result) == 2
        self._mock_txn_repo.get_by_user_id.assert_called_once_with(42)

    def test_get_transactions_by_user_id_empty(self) -> None:
        self._mock_txn_repo.get_by_user_id.return_value = []

        result = self._service.get_transactions_by_user_id(user_id=99)

        assert result == []
        self._mock_txn_repo.get_by_user_id.assert_called_once_with(99)

    def test_review_flagged_transaction_not_found(self) -> None:
        self._mock_txn_repo.get_by_id.return_value = None

        request = AdminReviewRequest(admin_username="admin1", action=AdminReviewAction.APPROVE)
        result = self._service.review_flagged_transaction(transaction_id=999, request=request)

        assert result.success is False
        assert "not found" in result.message.lower()

    def test_review_flagged_transaction_approve(self) -> None:
        txn = MagicMock()
        txn.id = 1
        txn.status = "pending"
        txn.amount = 100.0
        txn.initiator_id = 1
        txn.user_id = 1

        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(admin_username="admin1", action=AdminReviewAction.APPROVE)
        result = self._service.review_flagged_transaction(transaction_id=1, request=request)

        assert result.success is True
        assert result.new_status == "approved"
        assert "approved" in result.message

    def test_get_flagged_transactions_returns_pending(self) -> None:
        txn1 = MagicMock()
        txn1.id = 1
        txn1.status = "pending"
        txn1.amount = 100.0
        txn1.initiator_id = 1
        txn1.user_id = 1

        txn2 = MagicMock()
        txn2.id = 2
        txn2.status = "completed"
        txn2.amount = 50.0
        txn2.initiator_id = 1
        txn2.user_id = 1

        self._mock_txn_repo.get_all.return_value = [txn1, txn2]

        result = self._service.get_flagged_transactions()

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["status"] == "pending"
