from __future__ import annotations

import pytest
from decimal import Decimal
from datetime import datetime
from src.domain.withdrawal_transaction.WithdrawalTransaction import WithdrawalTransaction, WithdrawalStatus


class TestWithdrawalTransactionDomain:

    def test_create_withdrawal_transaction(self) -> None:
        """Test that a withdrawal transaction can be created with valid fields."""
        transaction = WithdrawalTransaction.create(
            account_id="acc-001",
            amount=Decimal("100.00")
        )
        assert transaction.id is not None
        assert transaction.account_id == "acc-001"
        assert transaction.amount == Decimal("100.00")
        assert transaction.status == WithdrawalStatus.PENDING
        assert transaction.timestamp is not None

    def test_create_with_zero_amount_raises_error(self) -> None:
        """Test that creating with zero amount raises ValueError."""
        with pytest.raises(ValueError, match="must be greater than 0"):
            WithdrawalTransaction.create(
                account_id="acc-001",
                amount=Decimal("0")
            )

    def test_create_with_negative_amount_raises_error(self) -> None:
        """Test that creating with negative amount raises ValueError."""
        with pytest.raises(ValueError, match="must be greater than 0"):
            WithdrawalTransaction.create(
                account_id="acc-001",
                amount=Decimal("-10.00")
            )

    def test_complete_transaction(self) -> None:
        """Test that a pending transaction can be marked as completed."""
        transaction = WithdrawalTransaction.create(
            account_id="acc-001",
            amount=Decimal("100.00")
        )
        transaction.complete()
        assert transaction.status == WithdrawalStatus.COMPLETED

    def test_fail_transaction(self) -> None:
        """Test that a pending transaction can be marked as failed."""
        transaction = WithdrawalTransaction.create(
            account_id="acc-001",
            amount=Decimal("100.00")
        )
        transaction.fail()
        assert transaction.status == WithdrawalStatus.FAILED

    def test_cannot_complete_failed_transaction(self) -> None:
        """Test that a failed transaction cannot be completed."""
        transaction = WithdrawalTransaction.create(
            account_id="acc-001",
            amount=Decimal("100.00")
        )
        transaction.fail()
        with pytest.raises(ValueError):
            transaction.complete()

    def test_cannot_fail_completed_transaction(self) -> None:
        """Test that a completed transaction cannot be failed."""
        transaction = WithdrawalTransaction.create(
            account_id="acc-001",
            amount=Decimal("100.00")
        )
        transaction.complete()
        with pytest.raises(ValueError):
            transaction.fail()

    def test_status_transitions(self) -> None:
        """Test valid transitions from WithdrawalStatus."""
        assert WithdrawalStatus.PENDING.can_transition_to(WithdrawalStatus.COMPLETED)
        assert WithdrawalStatus.PENDING.can_transition_to(WithdrawalStatus.FAILED)
        assert not WithdrawalStatus.COMPLETED.can_transition_to(WithdrawalStatus.PENDING)
        assert not WithdrawalStatus.COMPLETED.can_transition_to(WithdrawalStatus.PENDING)
        assert not WithdrawalStatus.FAILED.can_transition_to(WithdrawalStatus.COMPLETED)
