from __future__ import annotations

from typing import Any, TYPE_CHECKING, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid

if TYPE_CHECKING:
    from src.domain.account_flag import Resource
    from src.domain.user import User


class State(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class FailureReason(Enum):
    INSUFFICIENT_FUNDS = "insufficient_funds"
    NETWORK_ERROR = "network_error"
    SYSTEM_CRASH = "system_crash"
    LIMIT_EXCEEDED = "limit_exceeded"


class Role(Enum):
    INITIATOR = "initiator"
    APPROVER = "approver"
    VIEWER = "viewer"


class WithdrawalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class Money:
    amount: float
    currency: str = "USD"


@dataclass
class Transaction:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amount: Money = field(default_factory=lambda: Money(0))
    timestamp: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: State = State.PENDING


@dataclass
class WithdrawalRecord:
    transaction_id: str
    amount: Money
    status: WithdrawalStatus = WithdrawalStatus.PENDING
    failure_reason: Optional[FailureReason] = None


@dataclass
class TransactionId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class TransactionCreatedEvent:
    transaction: Transaction


@dataclass
class TransactionUpdatedEvent:
    transaction: Transaction
