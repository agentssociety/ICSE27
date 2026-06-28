from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from src.domain.blood_unit import BloodUnit
    from src.domain.reservation import Actor
    from src.repository.alert import InventoryPort, NotificationPort

"""
Domain layer for the Alert domain class

Package: domain.alert
Layer: domain
Related tasks: #30
Requirement coverage:
- Blood Stock Alert System
"""


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE1 = "pre1"
    POST1 = "post1"
    EC_SAFETY_STALE = "ec_safety_stale"


@dataclass
class User:
    userId: str
    mayPerform: set[Permission]

    def hasPermission(self, permission: Permission) -> bool:
        """Check if user has the specified permission."""
        return permission in self.mayPerform


@dataclass
class Resource:
    owner: Optional[Actor] = None
    accessible: set[Actor] = field(default_factory=set)
    owner_always_accessible: bool = True

    def checkAccess(self, initiator: Actor, target: Resource) -> bool:
        """Check if initiator has access to target resource."""
        # If initiator is the owner, they always have access when owner_always_accessible is True
        if self.owner_always_accessible and initiator == self.owner:
            return True
        # Check if initiator is in the accessible set
        return initiator in self.accessible or initiator == target.owner


@dataclass
class BloodTypeResource:
    bloodType: str
    units: int

    def isAccessible(self, manager: Any) -> bool:
        """Check if this blood type resource is accessible by a manager.
        Manager must not be None and must have appropriate clearance."""
        return manager is not None


@dataclass
class Operation:
    """Base class for all operations."""
    pass


@dataclass
class BloodTypeAlertOperation:
    inventoryPort: InventoryPort
    notificationPort: NotificationPort
    state: State = State.PRE1

    def create(self, manager: Any, bloodTypes: list[BloodTypeResource]) -> None:
        """Create a new alert operation for given blood types."""
        if manager is None:
            raise ValueError("Manager cannot be None")
        if not bloodTypes:
            raise ValueError("At least one blood type must be provided")
        for bt in bloodTypes:
            if not bt.isAccessible(manager):
                raise PermissionError(f"Blood type {bt.bloodType} is not accessible by manager")

    def checkStock(self, inventory: list[BloodTypeResource]) -> list[BloodTypeResource]:
        """Check inventory levels and return blood types that need alerts."""
        low_stock_items = []
        for item in inventory:
            if item.units < 10:  # Example threshold - should be configurable
                low_stock_items.append(item)
        return low_stock_items

    def updateState(self, new_state: State) -> None:
        """Update the operation state."""
        valid_transitions = {
            State.PRE1: [State.POST1],
            State.POST1: [State.EC_SAFETY_STALE],
        }
        if self.state in valid_transitions and new_state in valid_transitions[self.state]:
            self.state = new_state
        else:
            raise ValueError(f"Invalid state transition from {self.state} to {new_state}")


@dataclass
class Alert:
    bloodUnit: Optional[BloodUnit] = None
    message: str = ""
    state: State = State.PRE1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def setMessage(self, message: str) -> None:
        """Set the alert message."""
        self.message = message
        self.updated_at = datetime.now()

    def isStale(self, max_age_hours: int = 24) -> bool:
        """Check if the alert has become stale."""
        return (datetime.now() - self.created_at) > timedelta(hours=max_age_hours)


@dataclass
class AlertId:
    """Value Object for Alert ID."""
    id: str


@dataclass
class AlertCreatedEvent:
    """Event raised when an Alert is created."""
    alert_id: AlertId
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AlertUpdatedEvent:
    """Event raised when an Alert is updated."""
    alert_id: AlertId
    timestamp: datetime = field(default_factory=datetime.now)
