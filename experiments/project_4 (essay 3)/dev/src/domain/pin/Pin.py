from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from uuid import uuid4

if TYPE_CHECKING:
    from src.domain.authentication_attempt import AuthenticationAttempt
    from src.domain.card import Card

"""
Domain layer for the Pin domain class

Package: domain.pin
Layer: domain
Related tasks: #96
Requirement coverage:
- Account Lockout After 3 Consecutive Failed PIN Attempts
"""

MAX_FAILED_PIN_ATTEMPTS = 3


@dataclass
class User:
    """Represents a bank user who owns cards and has a PIN."""
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
class AuthenticationSession:
    """Represents an authentication session for PIN verification."""
    sessionId: str
    user: Optional[User] = None
    card: Optional[Any] = None
    consecutiveFailures: int = 0
    locked: bool = False
    field_invariants: str = "lockedimpliesconsecutiveFailures>=3"

    def __post_init__(self) -> None:
        if not self.sessionId:
            self.sessionId = str(uuid4())

    def create(self, card: Any, user: Any) -> AuthenticationSession:
        """Create a new authentication session for PIN verification."""
        return AuthenticationSession(
            sessionId=str(uuid4()),
            card=card,
            user=user,
            consecutiveFailures=0,
            locked=False
        )

    def resetConsecutiveFailures(self) -> None:
        """Reset consecutive failures on successful PIN entry."""
        self.consecutiveFailures = 0

    def incrementConsecutiveFailures(self) -> None:
        """Increment consecutive failures and lock if threshold reached."""
        self.consecutiveFailures += 1
        if self.consecutiveFailures >= MAX_FAILED_PIN_ATTEMPTS:
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
    """Records a failed PIN attempt."""
    device: Any = None  # Device
    operation: str = ""
    field_invariants: str = "Eachfailedattemptisrecorded"

    def createFailedAttempt(self, device: Any, operation: Any) -> None:
        """Record a failed PIN attempt."""
        self.device = device
        self.operation = str(operation)


@dataclass
class LockoutNotification:
    """Represents a lockout notification sent to the user after PIN failures."""
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


def hash_pin(pin: str) -> str:
    """Hash a PIN using SHA-256 for secure storage."""
    return sha256(pin.encode()).hexdigest()


@dataclass
class Pin:
    """Core domain model for a bank card PIN.

    Manages PIN verification, hashing, and lockout after consecutive
    failed attempts. PINs are stored as hashes for security.
    """
    account: Optional[Any] = None  # Account (forward reference)
    pin_hash: str = ""
    is_locked: bool = False
    failed_attempts: int = 0
    user_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Ensure the PIN object has a valid state."""
        if not self.pin_hash:
            # Allow creation without a pin_hash for placeholder pins
            pass

    @classmethod
    def create(cls, pin: str, user_id: str = "") -> Pin:
        """Factory method to create a new PIN from a plaintext value.

        The PIN is hashed immediately for secure storage.
        """
        if not pin or len(pin) < 4:
            raise ValueError("PIN must be at least 4 characters")
        if len(pin) > 8:
            raise ValueError("PIN must be at most 8 characters")
        if not pin.isdigit():
            raise ValueError("PIN must contain only digits")
        return cls(
            pin_hash=hash_pin(pin),
            is_locked=False,
            failed_attempts=0,
            user_id=user_id,
        )

    def verify(self, pin: str) -> bool:
        """Verify a provided PIN against the stored hash.

        Returns True if the PIN matches and the account is not locked.
        If the PIN does not match, increments the failed attempt counter.
        """
        if self.is_locked:
            return False
        if not pin or not self.pin_hash:
            return False
        if hash_pin(pin) == self.pin_hash:
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= MAX_FAILED_PIN_ATTEMPTS:
                self.is_locked = True
            return False

    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """Change the PIN after verifying the old PIN.

        Returns True if the change was successful, False otherwise.
        """
        if not self.verify(old_pin):
            return False
        self.pin_hash = hash_pin(new_pin)
        self.failed_attempts = 0
        self.is_locked = False
        return True

    def reset(self) -> None:
        """Reset the PIN lockout state (e.g., by admin intervention)."""
        self.failed_attempts = 0
        self.is_locked = False

    def is_valid_pin_format(self, pin: str) -> bool:
        """Check if a PIN string is in a valid format (4-8 digits)."""
        if not pin:
            return False
        if len(pin) < 4 or len(pin) > 8:
            return False
        return pin.isdigit()


@dataclass
class PinId:
    """Value object for PIN ID."""
    pass


@dataclass
class PinCreatedEvent:
    """Event emitted when a PIN is created."""
    pass


@dataclass
class PinUpdatedEvent:
    """Event emitted when a PIN is updated."""
    pass
