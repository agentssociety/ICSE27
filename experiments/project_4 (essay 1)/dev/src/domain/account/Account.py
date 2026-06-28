from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
import uuid

if TYPE_CHECKING:
    from src.domain.account_flag import Resource
    from src.domain.transaction import Transaction
    from src.domain.user import User


@dataclass
class Actor:
    mayPerform: set["Permission"]
    id: str
    name: str
    resources: list["Resource"] = field(default_factory=list)

    def displayFlaggedTransactions(self, lst: Any) -> None:
        pass

    def showConfirmation(self, Transaction_approved: Any) -> None:
        pass

    def showError(self, Cannot_act_on_escalated_transaction: Any) -> None:
        pass

    def showEmptyList(self, No_flagged_transactions: Any) -> None:
        pass

    def hasPermission(self, admin: "Actor", resource: "Resource", permission: "Permission") -> bool:
        return permission in admin.mayPerform


class AccountState(Enum):
    ACTIVE = "active"
    LOCKED = "locked"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class Account:
    failedAttempts: int = 0
    balance: float = 0.0
    daily_withdrawal_limit: float = 1000.0
    withdrawn_today: float = 0.0
    state: AccountState = AccountState.ACTIVE
    locked_reason: Optional[str] = None

    def authenticate(self) -> bool:
        if self.state == AccountState.LOCKED:
            return False
        return True

    def recordFailedAttempt(self) -> None:
        self.failedAttempts += 1
        if self.failedAttempts >= 3:
            self.state = AccountState.LOCKED

    def lock(self, reason: str = "") -> None:
        """Lock the account, preventing login. Records the reason for locking."""
        self.state = AccountState.LOCKED
        self.locked_reason = reason if reason else None

    def unlock(self) -> None:
        """Unlock the account, restoring full access. Clears the locked reason."""
        self.state = AccountState.ACTIVE
        self.locked_reason = None

    def has_sufficient_balance(self, amount: float) -> bool:
        return self.balance >= amount

    def has_daily_limit_remaining(self, amount: float) -> bool:
        return (self.withdrawn_today + amount) <= self.daily_withdrawal_limit

    def can_withdraw(self, amount: float) -> bool:
        return self.has_sufficient_balance(amount) and self.has_daily_limit_remaining(amount)

    def deduct_balance(self, amount: float) -> None:
        if not self.has_sufficient_balance(amount):
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def record_withdrawal(self, amount: float) -> None:
        self.withdrawn_today += amount


@dataclass
class AccountId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class AccountCreatedEvent:
    account: Account


@dataclass
class AccountUpdatedEvent:
    account: Account
