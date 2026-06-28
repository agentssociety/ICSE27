from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from src.domain.transaction.Transaction import (
    Transaction, FlaggedTransaction, System, FraudAnalyst,
    TransactionStatus, FlaggedTransactionStatus, Permission,
    RAPID_WITHDRAWAL_THRESHOLD_SECONDS, MAX_RAPID_WITHDRAWALS
)

"""
Unit tests for Transaction across domain, service, and API layers

Related tasks: #90, #92, #93
"""


class MockUser:
    """Mock user for testing."""
    def __init__(self):
        self.userId = "test-user-1"


def test_system_detects_rapid_withdrawals() -> None:
    system = System()
    user = MockUser()
    tx1 = Transaction(id="1", amount=Decimal("100"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx2 = Transaction(id="2", amount=Decimal("200"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx3 = Transaction(id="3", amount=Decimal("300"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    
    system.transactions = [tx1, tx2, tx3]
    assert system.checkFrequencyAndSpeed("acc-1", None) is True


def test_system_does_not_flag_normal_transactions() -> None:
    system = System()
    user = MockUser()
    tx1 = Transaction(id="1", amount=Decimal("100"), 
                      timestamp=datetime.utcnow() - timedelta(seconds=10),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx2 = Transaction(id="2", amount=Decimal("200"), 
                      timestamp=datetime.utcnow() - timedelta(seconds=8),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    
    system.transactions = [tx1, tx2]
    # 2 withdrawals is less than MAX_RAPID_WITHDRAWALS (3)
    assert system.checkFrequencyAndSpeed("acc-1", None) is False


def test_flagged_transaction_creation() -> None:
    user = MockUser()
    tx = Transaction(id="1", amount=Decimal("100"), timestamp=datetime.utcnow(),
                     accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    ft = FlaggedTransaction.create(None, tx)
    assert ft.transactionId == "1"
    assert ft.reviewStatus == FlaggedTransactionStatus.PENDING
    assert ft.status == TransactionStatus.FLAGGED
    assert "Suspicious pattern" in ft.flagReason


def test_flagged_transaction_status_change() -> None:
    user = MockUser()
    tx = Transaction(id="1", amount=Decimal("100"), timestamp=datetime.utcnow(),
                     accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    ft = FlaggedTransaction.create(None, tx)
    ft.changeStatus(FlaggedTransactionStatus.UNDER_REVIEW)
    assert ft.reviewStatus == FlaggedTransactionStatus.UNDER_REVIEW


def test_get_pending_flagged_transactions() -> None:
    system = System()
    user = MockUser()
    tx1 = Transaction(id="1", amount=Decimal("100"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx2 = Transaction(id="2", amount=Decimal("200"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    ft1 = FlaggedTransaction.create(None, tx1)
    ft2 = FlaggedTransaction.create(None, tx2)
    ft2.reviewStatus = FlaggedTransactionStatus.UNDER_REVIEW
    system.flaggedTransactions = [ft1, ft2]
    
    pending = system.getPendingFlaggedTransactions()
    assert len(pending) == 1
    assert pending[0].transactionId == "1"


def test_process_transaction_flags_suspicious() -> None:
    system = System()
    user = MockUser()
    tx1 = Transaction(id="1", amount=Decimal("100"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx2 = Transaction(id="2", amount=Decimal("200"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    tx3 = Transaction(id="3", amount=Decimal("300"), timestamp=datetime.utcnow(),
                      accountId="acc-1", status=TransactionStatus.NORMAL, user=user)
    
    system.processTransaction(tx1)
    system.processTransaction(tx2)
    assert len(system.flaggedTransactions) == 0  # Not enough yet
    system.processTransaction(tx3)
    assert len(system.flaggedTransactions) == 1  # Now flagged
