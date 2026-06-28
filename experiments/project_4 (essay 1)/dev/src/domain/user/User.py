from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
import uuid

if TYPE_CHECKING:
    from src.domain.account import Account
    from src.domain.account_flag import Resource
    from src.domain.card import Card
    from src.domain.pin import PIN
    from src.domain.transaction import Transaction


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


@dataclass
class User:
    userID: str
    card: "Card"
    pIN: "PIN"
    account: "Account"


class AccountState(Enum):
    ACTIVE = "active"
    LOCKED = "locked"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class UserId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class UserCreatedEvent:
    user: User


@dataclass
class UserUpdatedEvent:
    user: User
