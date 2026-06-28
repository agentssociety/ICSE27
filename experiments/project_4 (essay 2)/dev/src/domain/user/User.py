from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.account import Account, Admin, StateValue
    from src.domain.pin import Pin
    from src.domain.transaction import Transaction

"""
Domain layer for the User domain class

Package: domain.user
Layer: domain
Related tasks: #88, #89, #93, #94, #95
Requirement coverage:
- Card and PIN Authentication Requirement
- Account Lock After Three Consecutive Failed PIN Attempts
- Admin Interface for Flagged Transactions Review
- Manual Lock/Unlock User Accounts
- Audit Log Maintenance
"""


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE_IDLE = "pre_idle"
    POST_1 = "post_1"
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    PRE1 = "pre1"
    PRE2 = "pre2"
    PRE3 = "pre3"
    POST1 = "post1"
    POST2 = "post2"
    PREIDLE = "preidle"
    POST3 = "post3"


class IfaceKind(Enum):
    HARDWARE_INTERFACE = "hardware_interface"
    SERVICE_INTERFACE = "service_interface"


class Bool(Enum):
    TRUE_ = "true_"
    FALSE_ = "false_"


@dataclass
class Actor:
    mayPerform: set[Permission]

    def getActorByCard(self, cardData: str) -> Actor:
        # Simulate looking up an actor by card data
        return Actor(mayPerform={Permission.READ})

    def checkPermission(self, grant_Admin: Any) -> bool:
        # Check if actor has admin permission
        return Permission.ADMIN in self.mayPerform


@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]


@dataclass
class Credential:
    actor: Actor
    pin: Pin

    def getCredential(self, actor: Actor) -> Credential:
        return Credential(actor=actor, pin=self.pin)


@dataclass
class Digit:
    pin: Pin

    def transition(self, from_state: Any, to_state: Any) -> bool:
        # Simulate state transition for a digit
        return True


@dataclass
class User:
    userId: str
    account: str
    loginSession: str
    account_owns: Account
    transactions: list[Transaction] = field(default_factory=list)

    def createWithdrawalRequest(self) -> None:
        # Placeholder for withdrawal request creation
        pass


@dataclass
class UserId:
    pass


@dataclass
class UserCreatedEvent:
    pass


@dataclass
class UserUpdatedEvent:
    pass
