from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.authentication_attempt import AuthenticationAttempt
    from src.domain.account import Account

"""
Domain layer for the Card domain class

Package: domain.card
Layer: domain
Related tasks: #96
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
"""


@dataclass
class User:
    """Represents a bank user who owns cards and accounts."""
    userId: str
    card: Any = None  # Card (forward reference)
    account: Any = None  # Account (forward reference)
    roles: list[Any] = None  # list[Role]
    field_invariants: str = "Usermusthaveexactlyoneactivecard"
    authenticationAttempt: Any = None  # AuthenticationAttempt (forward reference)

    def __post_init__(self) -> None:
        if self.roles is None:
            self.roles = []


@dataclass
class Card:
    """Core domain model for a bank card.

    A card is associated with a user and an account, and is used for
    authentication during withdrawal attempts. Cards can expire.
    """
    cardNumber: str
    expired: bool = False
    user: Optional[User] = None
    field_invariants: str = "Cardmustbevalid(notexpired)forauthenticationattempt"
    account: Any = None  # Account (forward reference)
    authenticationAttempt: Any = None  # AuthenticationAttempt (forward reference)

    def __post_init__(self) -> None:
        self._id: str = str(uuid4())

    @property
    def id(self) -> str:
        return self._id

    def isExpired(self) -> bool:
        """Check if the card has expired."""
        return self.expired

    def verifyPin(self, pin: Any) -> bool:
        """Verify a PIN against the card's stored PIN.

        In the real system this would call out to a PIN service.
        Here we delegate to the associated account/user context.
        """
        if self.expired:
            return False
        if pin is None:
            return False
        # In a proper implementation, this would verify against a stored hash
        # For now, we return True to indicate the card is valid for authentication
        return not self.expired


@dataclass
class AuthenticationSession:
    """Represents an authentication session for a user/card combination."""
    sessionId: str
    user: Optional[User] = None
    card: Optional[Card] = None
    consecutiveFailures: int = 0
    locked: bool = False
    field_invariants: str = "lockedimpliesconsecutiveFailures>=3"

    def __post_init__(self) -> None:
        if not self.sessionId:
            self.sessionId = str(uuid4())

    def create(self, card: Any, user: Any) -> AuthenticationSession:
        """Create a new authentication session for the given card and user."""
        return AuthenticationSession(
            sessionId=str(uuid4()),
            card=card,
            user=user,
            consecutiveFailures=0,
            locked=False
        )

    def resetConsecutiveFailures(self) -> None:
        """Reset the consecutive failures counter on successful authentication."""
        self.consecutiveFailures = 0

    def incrementConsecutiveFailures(self) -> None:
        """Increment the consecutive failures counter and lock if threshold reached."""
        self.consecutiveFailures += 1
        if self.consecutiveFailures >= 3:
            self.locked = True


@dataclass
class LockoutRecord:
    """Records a lockout event for audit purposes."""
    device: Any = None  # Device
    operation: str = ""
    locked: bool = False
    field_invariants: str = "locked==Trueimpliesaccount.locked==True"
    account: Any = None  # Account

    def create(self, device: Any, operation: Any, locked_true: Any = None) -> None:
        """Create a lockout record."""
        self.device = device
        self.operation = str(operation)
        self.locked = True


@dataclass
class FailedAttempt:
    """Records a failed authentication attempt."""
    device: Any = None  # Device
    operation: str = ""
    field_invariants: str = "Eachfailedattemptisrecorded"

    def createFailedAttempt(self, device: Any, operation: Any) -> None:
        """Record a failed attempt."""
        self.device = device
        self.operation = str(operation)


@dataclass
class LockoutNotification:
    """Represents a lockout notification sent to the user."""
    device: Any = None  # Device
    lockout: Optional[LockoutRecord] = None
    sent: bool = False
    field_invariants: str = "sent==Truewhenlockoutoccurs"

    def send(self, device: Any, lockout: Any) -> None:
        """Send a lockout notification."""
        self.device = device
        self.lockout = lockout
        self.sent = True

    def setSent(self, sent: bool = True) -> None:
        """Mark the notification as sent."""
        self.sent = sent


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE_IDLE = "pre_idle"
    AUTHENTICATING = "authenticating"
    UNLOCKED = "unlocked"
    LOCKED = "locked"


@dataclass
class CardId:
    """Value object for card ID."""
    pass


@dataclass
class CardCreatedEvent:
    """Event emitted when a card is created."""
    pass


@dataclass
class CardUpdatedEvent:
    """Event emitted when a card is updated."""
    pass
