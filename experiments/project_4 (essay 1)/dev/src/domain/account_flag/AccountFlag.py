
from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from src.domain.account import Account
    from src.domain.transaction import Transaction


class FlagReason(Enum):
    RAPID_CONSECUTIVE_WITHDRAWALS = "rapid_consecutive_withdrawals"
    UNUSUAL_AMOUNT = "unusual_amount"
    MANUAL_REVIEW = "manual_review"


@dataclass
class AccountFlag:
    account_id: int
    transaction_id: Optional[str] = None
    reason: FlagReason = FlagReason.MANUAL_REVIEW
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def matches_reason(self, reason: FlagReason) -> bool:
        return self.reason == reason


@dataclass
class AccountFlagId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class AccountFlagCreatedEvent:
    flag: AccountFlag


@dataclass
class AccountFlagUpdatedEvent:
    flag: AccountFlag
