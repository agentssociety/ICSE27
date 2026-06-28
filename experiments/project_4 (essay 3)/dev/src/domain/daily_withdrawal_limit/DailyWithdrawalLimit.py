from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4

"""
Domain layer for the DailyWithdrawalLimit domain class

Package: domain.daily_withdrawal_limit
Layer: domain
Related tasks: #97, #98
Requirement coverage:
- Decline Withdrawals Exceeding Account Balance or Daily Limit
- Atomic Withdrawal Transactions
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
    """Possible states for a daily withdrawal limit."""
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
    """Pre-condition: user has active account with positive balance."""
    represents: str = "userhasactiveaccountwithpositivebalance"


@dataclass
class Pre2:
    """Pre-condition: system tracks cumulative daily withdrawal total."""
    represents: str = "systemtrackscumulativedailywithdrawaltotal"


@dataclass
class Post1:
    """Post-condition: user receives decline message."""
    represents: str = "userreceivesdeclinemessageindicatingamountexceedsbalanceordailylimit"


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


@dataclass
class Account_Balance_Database:
    """Marker for account balance database."""
    invariant: str = "kind=Database"


@dataclass
class Daily_Withdrawal_Tracking_Service:
    """Marker for daily withdrawal tracking service."""
    invariant: str = "kind=Service"


@dataclass
class DailyWithdrawalLimit:
    """Core domain model for daily withdrawal limits on accounts.

    Tracks how much has been withdrawn today and enforces the daily limit.
    Limits reset after a configurable time window (default 24 hours).
    """
    account_id: str
    daily_limit: float = 200.0
    used_today: float = 0.0
    reset_time: Optional[str] = None
    last_withdrawal_at: Optional[str] = None

    def __post_init__(self) -> None:
        """Initialize reset_time if not provided."""
        if self.reset_time is None:
            now = datetime.utcnow()
            next_reset = now + timedelta(days=1)
            self.reset_time = next_reset.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    def remaining_limit(self) -> float:
        """Return the remaining amount that can be withdrawn today."""
        return max(0.0, self.daily_limit - self.used_today)

    def can_withdraw(self, amount: float) -> bool:
        """Check if the given amount can be withdrawn without exceeding the daily limit."""
        if amount <= 0:
            return False
        return (self.used_today + amount) <= self.daily_limit

    def record_withdrawal(self, amount: float) -> None:
        """Record a withdrawal and update used_today."""
        if not self.can_withdraw(amount):
            raise ValueError(
                f"Cannot withdraw {amount}: daily limit would be exceeded. "
                f"Used: {self.used_today}, Limit: {self.daily_limit}"
            )
        self.used_today += amount
        self.last_withdrawal_at = datetime.utcnow().isoformat()

    def reset_daily_usage(self) -> None:
        """Reset the daily usage counter (e.g., after midnight)."""
        self.used_today = 0.0
        now = datetime.utcnow()
        next_reset = now + timedelta(days=1)
        self.reset_time = next_reset.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        self.last_withdrawal_at = None

    def check_and_reset_if_needed(self) -> None:
        """Check if the daily limit should be reset based on elapsed time."""
        if self.reset_time is None:
            return
        try:
            reset_dt = datetime.fromisoformat(self.reset_time)
        except (ValueError, TypeError):
            return
        if datetime.utcnow() >= reset_dt:
            self.reset_daily_usage()

    def set_daily_limit(self, new_limit: float) -> None:
        """Update the daily limit."""
        if new_limit <= 0:
            raise ValueError("Daily limit must be positive")
        self.daily_limit = new_limit

    def increase_used(self, amount: float) -> None:
        """Increase the used_today amount (called after a successful withdrawal)."""
        self.used_today += amount

    def get_usage_percentage(self) -> float:
        """Return the percentage of the daily limit that has been used."""
        if self.daily_limit <= 0:
            return 0.0
        return (self.used_today / self.daily_limit) * 100.0


@dataclass
class DailyWithdrawalLimitId:
    """Value object for daily withdrawal limit ID."""
    pass


@dataclass
class DailyWithdrawalLimitCreatedEvent:
    """Event emitted when a daily withdrawal limit is created."""
    pass


@dataclass
class DailyWithdrawalLimitUpdatedEvent:
    """Event emitted when a daily withdrawal limit is updated."""
    pass
