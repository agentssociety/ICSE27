from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

if TYPE_CHECKING:
    from src.domain.account import Account
    from src.domain.card import Card
    from src.domain.pin import PIN
    from src.domain.user import User


class AuditActionType(Enum):
    """Types of auditable security events"""
    AUTHENTICATION_SUCCESS = "authentication_success"
    AUTHENTICATION_FAILURE = "authentication_failure"
    ACCOUNT_LOCKED = "account_locked"
    ACCOUNT_UNLOCKED = "account_unlocked"
    TRANSACTION_APPROVED = "transaction_approved"
    TRANSACTION_REJECTED = "transaction_rejected"
    TRANSACTION_ESCALATED = "transaction_escalated"
    FLAGGED_TRANSACTION_REVIEWED = "flagged_transaction_reviewed"


@dataclass
class AuditLogEntry:
    operation: str
    timestamp: datetime
    username: str
    ip_address: str
    outcome: str
    user_id: Optional[str] = None
    account_id: Optional[int] = None
    action_type: Optional[str] = None

    def __post_init__(self) -> None:
        if self.action_type is None:
            self.action_type = AuditActionType.AUTHENTICATION_SUCCESS.value


@dataclass
class AuditLogEntryId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class AuditLogEntryCreatedEvent:
    entry: AuditLogEntry


@dataclass
class AuditLogEntryUpdatedEvent:
    entry: AuditLogEntry
