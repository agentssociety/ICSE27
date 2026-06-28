from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from src.domain.blood_unit import BloodUnit

"""
Domain layer for the Reservation domain class

Package: domain.reservation
Layer: domain
Related tasks: #28
Requirement coverage:
- Automatic Release of Reserved Units for Scheduled Transfusions
"""


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class IfaceKind(Enum):
    API = "api"
    DATABASE = "database"


@dataclass(frozen=True)
class State:
    name: str

    def checkStateChange(self, pre: State, post: State) -> bool:
        """Check if a state transition from pre to post is valid."""
        valid_transitions: dict[str, list[str]] = {
            "Reserved": ["Available", "Canceled", "Completed"],
            "Available": ["Reserved"],
            "Canceled": ["Reserved"],
            "Completed": [],
            "Expired": [],
        }
        if pre.name not in valid_transitions:
            return False
        return post.name in valid_transitions[pre.name]

    def transitionState(self, pre: State, post: State) -> State:
        """Transition from one state to another if valid."""
        if not self.checkStateChange(pre, post):
            raise ValueError(f"Invalid state transition from {pre.name} to {post.name}")
        return post

    @classmethod
    def reserved(cls) -> State:
        return cls(name="Reserved")

    @classmethod
    def available(cls) -> State:
        return cls(name="Available")

    @classmethod
    def canceled(cls) -> State:
        return cls(name="Canceled")

    @classmethod
    def completed(cls) -> State:
        return cls(name="Completed")

    @classmethod
    def expired(cls) -> State:
        return cls(name="Expired")


@dataclass(frozen=True)
class Actor:
    actorId: str
    mayPerform: frozenset[Permission]

    def checkPermission(self, initiator: Optional[Actor], grant: Permission) -> bool:
        """Check if initiator has the specified permission."""
        if initiator is None:
            return False
        return grant in initiator.mayPerform


@dataclass
class Resource:
    owner: Optional[Actor] = None
    accessible: set[Actor] = field(default_factory=set)
    owner_always_accessible: bool = True

    def checkAccess(self, initiator: Optional[Actor], target: Resource) -> bool:
        """Check if initiator has access to target resource."""
        if initiator is None:
            return False
        # If initiator is the owner, they always have access
        if target.owner is not None and target.owner_always_accessible and initiator.actorId == target.owner.actorId:
            return True
        # Check if initiator is in the accessible set by actorId
        return any(a.actorId == initiator.actorId for a in target.accessible)


@dataclass(frozen=True)
class Interface:
    kind: IfaceKind
    encrypted: bool = False
    authenticated: bool = False

    def checkAuthentication(self, channel: Interface) -> bool:
        """Check if the channel is authenticated."""
        return channel.authenticated


@dataclass
class Scheduling_API:
    """Represents the scheduling API for managing reservations."""
    pass


@dataclass
class Blood_Inventory_Database:
    """Represents the blood inventory database for querying and modifying reservations."""

    def queryReservation(self, unitId: str) -> State:
        """Query the current state of a reservation for a blood unit."""
        return State.available()

    def releaseReservation(self, unitId: str) -> bool:
        """Release a reservation for a blood unit."""
        return True

    def updateReservationStatus(self, unitId: str, new_state: State) -> bool:
        """Update the reservation status of a blood unit."""
        return True


@dataclass
class REQ_BB_01:
    """Operation representing a blood bank reservation request with invariants."""
    initiator: Actor
    target: list[Resource]
    channel: set[Interface]
    grant: Permission
    pre: State
    post: State

    def _validate_invariants(self) -> None:
        """Validate all business invariants for this operation."""
        if not self.channel:
            raise ValueError("Operation requires at least one channel")
        
        if not self.target:
            raise ValueError("Operation requires at least one target resource")
        
        # Inv: initiator must be authorized
        if not self.initiator.checkPermission(self.initiator, self.grant):
            raise PermissionError(f"Initiator does not have {self.grant.value} permission")
        
        # Inv: resource access control
        for resource in self.target:
            if not resource.checkAccess(self.initiator, resource):
                raise PermissionError("Initiator does not have access to target resource")
        
        # Inv: at least one state change must occur
        if self.pre == self.post:
            raise ValueError("Operation must involve at least one state change (pre != post)")

    def createOperation(self) -> None:
        """Create the operation and validate all invariants."""
        self._validate_invariants()


@dataclass
class CancellationRecord:
    """Record of a cancellation operation."""
    op: REQ_BB_01
    resource: Resource
    time: State

    @classmethod
    def createCancellationRecord(cls, op: REQ_BB_01, resource: Resource, time_state: State) -> CancellationRecord:
        """Create a cancellation record for an operation."""
        if op.grant != Permission.WRITE and op.grant != Permission.ADMIN:
            raise PermissionError("Cancellation requires WRITE or ADMIN permission")
        return cls(op=op, resource=resource, time=time_state)


@dataclass
class OverlapRecord:
    """Record of an overlap conflict between two operations."""
    resource: Resource
    first: REQ_BB_01
    second: REQ_BB_01

    @classmethod
    def recordOverlap(cls, resource: Resource, first_op: REQ_BB_01, second_op: REQ_BB_01) -> OverlapRecord:
        """Record an overlap between two operations on the same resource."""
        if resource not in first_op.target or resource not in second_op.target:
            raise ValueError("Resource must be a target of both operations")
        return cls(resource=resource, first=first_op, second=second_op)


@dataclass
class OutageRecord:
    """Record of a system outage that affected an operation."""
    op: Optional[REQ_BB_01]
    reason: str

    @classmethod
    def createOutageRecord(cls, op: Optional[REQ_BB_01], reason: str) -> OutageRecord:
        """Create an outage record for a failed operation."""
        if not reason:
            raise ValueError("Reason for outage must be provided")
        return cls(op=op, reason=reason)


@dataclass
class Reservation:
    bloodUnit: Optional[BloodUnit] = None
    state: State = field(default_factory=State.available)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def setState(self, new_state: State) -> None:
        """Set the reservation state with validation."""
        if not self.state.checkStateChange(self.state, new_state):
            raise ValueError(f"Invalid state transition from {self.state.name} to {new_state.name}")
        self.state = new_state
        self.updated_at = datetime.now()


@dataclass
class ReservationId:
    """Value Object for Reservation ID."""
    id: str


@dataclass
class ReservationCreatedEvent:
    """Event raised when a Reservation is created."""
    reservation_id: ReservationId
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ReservationUpdatedEvent:
    """Event raised when a Reservation is updated."""
    reservation_id: ReservationId
    timestamp: datetime = field(default_factory=datetime.now)
