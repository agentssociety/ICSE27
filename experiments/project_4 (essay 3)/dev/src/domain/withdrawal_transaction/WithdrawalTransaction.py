from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

"""
Domain layer for the WithdrawalTransaction domain class

Package: domain.withdrawal_transaction
Layer: domain
Related tasks: #98, #99, #100
Requirement coverage:
- Atomic Withdrawal Transactions
- Detection and Flagging of Suspicious Withdrawal Patterns
- Admin User Management and Transaction Review
"""

class WithdrawalStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

    def can_transition_to(self, new_status: WithdrawalStatus) -> bool:
        """Validates state transitions."""
        valid_transitions = {
            WithdrawalStatus.PENDING: [WithdrawalStatus.COMPLETED, WithdrawalStatus.FAILED],
        }
        return new_status in valid_transitions.get(self, [])


@dataclass
class WithdrawalTransaction:
    id: str
    account_id: str
    amount: Decimal
    status: WithdrawalStatus
    timestamp: datetime

    @classmethod
    def create(cls, account_id: str, amount: Decimal) -> WithdrawalTransaction:
        """Factory method to create a new withdrawal transaction."""
        if amount <= Decimal('0'):
            raise ValueError("Withdrawal amount must be greater than 0")
        return cls(
            id=str(uuid4()),
            account_id=account_id,
            amount=amount,
            status=WithdrawalStatus.PENDING,
            timestamp=datetime.utcnow()
        )

    def complete(self) -> None:
        """Mark the transaction as completed."""
        if not self.status.can_transition_to(WithdrawalStatus.COMPLETED):
            raise ValueError(f"Cannot transition from {self.status.value} to completed")
        self.status = WithdrawalStatus.COMPLETED

    def fail(self) -> None:
        """Mark the transaction as failed."""
        if not self.status.can_transition_to(WithdrawalStatus.FAILED):
            raise ValueError(f"Cannot transition from {self.status.value} to failed")
        self.status = WithdrawalStatus.FAILED


@dataclass
class WithdrawalTransactionId:
    """Value object for withdrawal transaction ID."""
    pass


@dataclass
class WithdrawalTransactionCreatedEvent:
    """Event emitted when a withdrawal transaction is created."""
    pass


@dataclass
class WithdrawalTransactionUpdatedEvent:
    """Event emitted when a withdrawal transaction is updated."""
    pass
