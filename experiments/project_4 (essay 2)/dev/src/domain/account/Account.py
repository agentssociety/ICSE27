from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.transaction import Transaction
    from src.domain.user import User
    from src.repository.account import Interface

"""
Domain layer for the Account domain class

Package: domain.account
Layer: domain
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""

MAX_FAILED_PIN_ATTEMPTS = 3


class LockStatus(Enum):
    UNLOCKED = "unlocked"
    LOCKED = "locked"


class PermissionType(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    FIELD_ADMIN_SUBSUMES_ALL_OTHERS = "field_admin_subsumes_all_others"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"


class StateValue(Enum):
    PRE1 = "pre1"
    POST0 = "post0"
    POST1 = "post1"


class AccountStatus(Enum):
    ACTIVE = "active"
    LOCKED = "locked"


@dataclass
class Account:
    lockStatus: LockStatus
    failedAttemptCount: int
    consecutiveFailedCount: int
    field_invariants: Any
    balance: int
    dailyLimit: int
    usedToday: int
    user: User
    transaction: Optional[Transaction] = None

    def checkSufficientFunds(self, balance: int, amount: int) -> bool:
        return balance >= amount

    def checkDailyLimit(self, usedToday: int, dailyLimit: int, amount: int) -> bool:
        return (usedToday + amount) <= dailyLimit

    def updateBalance(self, amount: int) -> Account:
        return Account(
            lockStatus=self.lockStatus,
            failedAttemptCount=self.failedAttemptCount,
            consecutiveFailedCount=self.consecutiveFailedCount,
            field_invariants=self.field_invariants,
            balance=self.balance - amount,
            dailyLimit=self.dailyLimit,
            usedToday=self.usedToday + amount,
            user=self.user,
        )

    def updateUsedToday(self, amount: int) -> Account:
        return Account(
            lockStatus=self.lockStatus,
            failedAttemptCount=self.failedAttemptCount,
            consecutiveFailedCount=self.consecutiveFailedCount,
            field_invariants=self.field_invariants,
            balance=self.balance,
            dailyLimit=self.dailyLimit,
            usedToday=self.usedToday + amount,
            user=self.user,
        )

    def record_failed_attempt(self) -> None:
        self.consecutiveFailedCount += 1
        self.failedAttemptCount += 1
        if self.consecutiveFailedCount >= MAX_FAILED_PIN_ATTEMPTS:
            self.lockStatus = LockStatus.LOCKED

    def reset_failed_attempts(self) -> None:
        self.consecutiveFailedCount = 0


@dataclass
class Actor:
    actorId: str
    mayPerform: set[Permission]
    account: Account

    def getPermissions(self, actorId: str) -> set[Permission]:
        return self.mayPerform


@dataclass
class Resource:
    resourceId: str
    owner: Actor
    accessible: set[Actor]

    def checkAccess(self, actorId: str, accountId: str) -> bool:
        return any(a.actorId == actorId for a in self.accessible)


@dataclass
class Operation:
    operationId: str
    preCondition: State
    postCondition: State
    initiator: Actor
    target: Account
    transaction: Transaction
    interfaces: list[Interface]
    permission: Permission
    preState: State
    postState: State

    def createOperation(self, state: State.Pre2, result: State.Post2) -> None:
        pass


@dataclass
class FailedAttempt:
    actor: Actor
    count: int
    field_invariants: Any


@dataclass
class UserAccount:
    status: AccountStatus
    abstract_owner: Admin

    def load(self, accountId: Any) -> None:
        pass

    def getOwner(self) -> None:
        pass

    def getStatus(self) -> AccountStatus:
        return self.status

    def lock(self) -> None:
        self.status = AccountStatus.LOCKED

    def unlock(self) -> None:
        self.status = AccountStatus.ACTIVE

    def updateStatus(self) -> None:
        pass

    def success(self, version_becomes_2: Any) -> None:
        pass


@dataclass
class Admin:
    pass


@dataclass
class SecurityTeam:
    pass


@dataclass
class AccountId:
    pass


@dataclass
class AccountCreatedEvent:
    pass


@dataclass
class AccountUpdatedEvent:
    pass
