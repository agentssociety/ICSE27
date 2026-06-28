from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from src.service.transaction.transaction_service import (
    TransactionServiceImpl,
    AdminReviewRequest,
    AdminReviewAction,
    AdminReviewResponse,
)


class TestAdminReview:
    def setup_method(self) -> None:
        self._mock_txn_repo = MagicMock()
        self._mock_account_repo = MagicMock()
        self._mock_audit_repo = MagicMock()
        self._service = TransactionServiceImpl(
            transaction_repo=self._mock_txn_repo,
            account_repo=self._mock_account_repo,
            audit_repo=self._mock_audit_repo,
        )

    def test_approve_flagged_transaction(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 1
        txn.status = "pending"
        txn.amount = 100.0
        txn.initiator_id = 1
        txn.user_id = 1
        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.APPROVE, admin_username="admin1")

        # Act
        result = self._service.review_flagged_transaction(1, request)

        # Assert
        assert result.success is True
        assert result.new_status == "approved"
        assert result.transaction_id == 1
        self._mock_txn_repo.update.assert_called_once()
        self._mock_audit_repo.create.assert_called_once()

    def test_reject_flagged_transaction(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 2
        txn.status = "pending"
        txn.amount = 50.0
        txn.initiator_id = 1
        txn.user_id = 1
        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.REJECT, admin_username="admin2")

        # Act
        result = self._service.review_flagged_transaction(2, request)

        # Assert
        assert result.success is True
        assert result.new_status == "rejected"
        assert result.transaction_id == 2
        self._mock_txn_repo.update.assert_called_once()
        self._mock_audit_repo.create.assert_called_once()

    def test_escalate_flagged_transaction(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 3
        txn.status = "flagged"
        txn.amount = 200.0
        txn.initiator_id = 1
        txn.user_id = 1
        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.ESCALATE, admin_username="admin3")

        # Act
        result = self._service.review_flagged_transaction(3, request)

        # Assert
        assert result.success is True
        assert result.new_status == "escalated"
        assert result.transaction_id == 3
        self._mock_txn_repo.update.assert_called_once()
        self._mock_audit_repo.create.assert_called_once()

    def test_review_nonexistent_transaction(self) -> None:
        # Arrange
        self._mock_txn_repo.get_by_id.return_value = None

        request = AdminReviewRequest(action=AdminReviewAction.APPROVE, admin_username="admin")

        # Act
        result = self._service.review_flagged_transaction(999, request)

        # Assert
        assert result.success is False
        assert "not found" in result.message
        self._mock_txn_repo.update.assert_not_called()
        self._mock_audit_repo.create.assert_not_called()

    def test_cannot_review_already_approved(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 4
        txn.status = "approved"
        self._mock_txn_repo.get_by_id.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.REJECT, admin_username="admin")

        # Act
        result = self._service.review_flagged_transaction(4, request)

        # Assert
        assert result.success is False
        assert "Cannot act on" in result.message
        assert "approved" in result.message
        self._mock_txn_repo.update.assert_not_called()
        self._mock_audit_repo.create.assert_not_called()

    def test_cannot_review_already_rejected(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 5
        txn.status = "rejected"
        self._mock_txn_repo.get_by_id.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.APPROVE, admin_username="admin")

        # Act
        result = self._service.review_flagged_transaction(5, request)

        # Assert
        assert result.success is False
        assert "Cannot act on" in result.message
        self._mock_txn_repo.update.assert_not_called()

    def test_cannot_review_escalated(self) -> None:
        # Arrange
        txn = MagicMock()
        txn.id = 6
        txn.status = "escalated"
        self._mock_txn_repo.get_by_id.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.ESCALATE, admin_username="admin")

        # Act
        result = self._service.review_flagged_transaction(6, request)

        # Assert
        assert result.success is False
        assert "Cannot act on" in result.message
        self._mock_txn_repo.update.assert_not_called()

    def test_audit_logged_on_review(self) -> None:
        """Verify the audit log entry is created with correct details."""
        # Arrange
        txn = MagicMock()
        txn.id = 10
        txn.status = "pending"
        txn.amount = 150.0
        txn.initiator_id = 1
        txn.user_id = 1
        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.APPROVE, admin_username="auditor1")

        # Act
        result = self._service.review_flagged_transaction(10, request)

        # Assert
        assert result.success is True
        # Verify audit was called
        self._mock_audit_repo.create.assert_called_once()
        call_args = self._mock_audit_repo.create.call_args[0][0]
        assert "auditor1" in call_args.operation
        assert "approved" in call_args.operation

    def test_audit_not_logged_when_no_audit_repo(self) -> None:
        """If no audit_repo is provided, the review should still work."""
        service_no_audit = TransactionServiceImpl(
            transaction_repo=self._mock_txn_repo,
            account_repo=self._mock_account_repo,
            audit_repo=None,
        )
        txn = MagicMock()
        txn.id = 11
        txn.status = "pending"
        txn.amount = 100.0
        txn.initiator_id = 1
        txn.user_id = 1
        self._mock_txn_repo.get_by_id.return_value = txn
        self._mock_txn_repo.update.return_value = txn

        request = AdminReviewRequest(action=AdminReviewAction.REJECT, admin_username="admin")

        # Act
        result = service_no_audit.review_flagged_transaction(11, request)

        # Assert
        assert result.success is True
        assert result.new_status == "rejected"
