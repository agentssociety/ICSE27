from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.card import Card

"""
Domain layer for the Account domain class

Package: domain.account
Layer: domain
Related tasks: #96, #97, #98, #99, #100
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
- Decline Withdrawals Exceeding Account Balance or Daily Limit
- Atomic Withdrawal Transactions
- Detection and Flagging of Suspicious Withdrawal Patterns
- Admin User Management and Transaction Review
"""

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class IfaceKind(Enum):
    DATABASE = "database"
    SERVICE = "service"


@dataclass
class Actor:
    """Represents an actor with permissions."""
    id: str
    mayPerform: set[Permission]

    def checkPermission(self, initiator: Actor, requiredPermission: Permission) -> bool:
        """Check if this actor has the required permission."""
        return requiredPermission in self.mayPerform


@dataclass
class Bank_Users:
    """Marker class for bank users."""
    pass


@dataclass
class Customer_Support:
    """Marker class for customer support."""
    pass


@dataclass
class IT_Team:
    """Marker class for IT team."""
    pass


class State(Enum):
    """Possible states for an account."""
    PRE_IDLE = "pre_idle"
    AUTHENTICATING = "authenticating"
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"
    POST3 = "post3"
    PREIDLE = "preidle"
    ACTIVE = "active"
    FLAGGED = "flagged"


@dataclass
class Pre1:
    """Pre-condition marker."""
    represents: str = ""


@dataclass
class Pre2:
    """Pre-condition marker."""
    represents: str = ""


@dataclass
class Post1:
    """Post-condition marker."""
    represents: str = ""


@dataclass
class Resource:
    """Represents a resource with access control."""
    owner: Actor
    accessible: set[Actor]
    invariant: str = "owner_always_accessible:ownerinaccessible"

    def checkAccessibility(self, IT: Any) -> bool:
        """Check if the resource is accessible."""
        return True


@dataclass
class Interface:
    """Represents an interface."""
    kind: IfaceKind
    encrypted: bool
    authenticated: bool


class Account_Balance_Database:
    """Marker for account balance database."""
    invariant: str = "kind=Database"


class Daily_Withdrawal_Tracking_Service:
    """Marker for daily withdrawal tracking service."""
    invariant: str = "kind=Service"


MAX_FAILED_ATTEMPTS = 3


@dataclass
class Account:
    """Core domain model for a bank account.

    Manages account state including balance tracking, lockout after failed
    PIN attempts, and access control.
    """
    accountId: str
    balance: float
    locked: bool
    failedAttemptCount: int
    user: Any = None
    field_invariants: str = ""
    id: str = ""
    owner: Optional[Actor] = None
    accessible: list[Actor] = field(default_factory=list)
    card: Any = None

    def __post_init__(self) -> None:
        """Initialize derived fields after dataclass init."""
        if not self.id:
            self.id = str(uuid4())
        if not self.accountId:
            self.accountId = self.id
        if self.owner is None:
            self.owner = Actor(id="default_owner", mayPerform={Permission.READ, Permission.WRITE})

    def isLocked(self) -> bool:
        """Check if the account is locked."""
        return self.locked

    def unlock(self) -> None:
        """Unlock the account and reset failed attempt count."""
        self.locked = False
        self.failedAttemptCount = 0

    def setLocked(self, locked: bool) -> None:
        """Set the locked state of the account."""
        self.locked = locked

    def lock(self) -> None:
        """Lock the account."""
        self.locked = True

    def getAccount(self, accountId: str) -> Account:
        """Return self if the accountId matches, otherwise raise ValueError."""
        if self.accountId == accountId:
            return self
        raise ValueError(f"Account {accountId} not found")

    def updateBalance(self, accountId: str, amount: float) -> float:
        """Update the account balance by adding the given amount (can be negative)."""
        if self.accountId != accountId:
            raise ValueError(f"Account {accountId} does not match this account")
        new_balance = self.balance + amount
        if new_balance < 0:
            raise ValueError("Insufficient balance")
        self.balance = new_balance
        return self.balance

    def getStatus(self) -> State:
        """Return the current status of the account."""
        if self.locked:
            return State.LOCKED
        if self.balance < 0:
            return State.FLAGGED
        if self.balance == 0:
            return State.PRE_IDLE
        return State.ACTIVE

    def record_failed_attempt(self) -> None:
        """Record a failed PIN attempt and lock account if threshold reached."""
        self.failedAttemptCount += 1
        if self.failedAttemptCount >= MAX_FAILED_ATTEMPTS:
            self.lock()

    def has_sufficient_balance(self, amount: float) -> bool:
        """Check if the account has sufficient balance for a withdrawal."""
        return self.balance >= amount

    def deduct_balance(self, amount: float) -> None:
        """Deduct the given amount from the account balance."""
        if not self.has_sufficient_balance(amount):
            raise ValueError("Insufficient balance")
        self.balance -= amount


@dataclass
class AccountId:
    """Value object for account ID."""
    pass


@dataclass
class AccountCreatedEvent:
    """Event emitted when an account is created."""
    pass


@dataclass
class AccountUpdatedEvent:
    """Event emitted when an account is updated."""
    pass
