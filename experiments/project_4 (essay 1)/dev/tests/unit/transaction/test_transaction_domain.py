from __future__ import annotations

import pytest
from src.domain.transaction import Transaction, State, Money, FailureReason, WithdrawalRecord, WithdrawalStatus, TransactionId


class TestTransactionDomain:
    def test_transaction_initial_state_is_pending(self) -> None:
        transaction = Transaction()
        assert transaction.status == State.PENDING

    def test_transaction_has_unique_id(self) -> None:
        t1 = Transaction()
        t2 = Transaction()
        assert t1.transaction_id != t2.transaction_id

    def test_money_default_currency(self) -> None:
        money = Money(amount=100.0)
        assert money.currency == "USD"
        assert money.amount == 100.0

    def test_withdrawal_record_default_status(self) -> None:
        record = WithdrawalRecord(
            transaction_id="txn-123",
            amount=Money(amount=50.0)
        )
        assert record.status == WithdrawalStatus.PENDING
        assert record.failure_reason is None

    def test_withdrawal_record_with_failure(self) -> None:
        record = WithdrawalRecord(
            transaction_id="txn-456",
            amount=Money(amount=75.0),
            status=WithdrawalStatus.REJECTED,
            failure_reason=FailureReason.INSUFFICIENT_FUNDS
        )
        assert record.status == WithdrawalStatus.REJECTED
        assert record.failure_reason == FailureReason.INSUFFICIENT_FUNDS

    def test_transaction_state_enum_values(self) -> None:
        assert State.PENDING.value == "pending"
        assert State.COMPLETED.value == "completed"
        assert State.FAILED.value == "failed"
        assert State.ROLLED_BACK.value == "rolled_back"

    def test_failure_reason_enum_values(self) -> None:
        assert FailureReason.NETWORK_ERROR.value == "network_error"
        assert FailureReason.SYSTEM_CRASH.value == "system_crash"
        assert FailureReason.LIMIT_EXCEEDED.value == "limit_exceeded"
