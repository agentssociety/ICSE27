from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

"""
Domain layer for the Slot domain class

Package: domain.slot
Layer: domain
Related tasks: #47, #48, #49, #50, #51, #52
Requirement coverage:
- Automate Earliest Available Time Slot Allocation with Gap
- Priority Slot Allocation for Arrival Flights
- Prevent Overlapping Flight Assignments
- Automatic Reassignment of Flights During Runway Closure
- Handle Emergency Flights
"""

SLOT_DURATION_MINUTES = 5
GAP_MINUTES = 3

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

@dataclass
class Actor:
    mayPerform: list[Permission]

@dataclass
class Resource:
    owner: Actor
    accessible: list[Actor]
    slot: Slot | None = None

    def createFrom(self, scheduleData: Any) -> "Slot":
        """Create a slot from schedule data."""
        if not scheduleData:
            raise ValueError("scheduleData must not be empty")
        slot_time = scheduleData.get('time', 0) if isinstance(scheduleData, dict) else getattr(scheduleData, 'time', 0)
        new_slot = Slot()
        new_slot.create(time=slot_time, resource=self)
        self.slot = new_slot
        return new_slot

@dataclass
class Slot:
    resource: Resource | None = None
    isAvailable: bool = True
    time: int = 0

    def create(self, time: int, resource: Resource) -> None:
        """Initialize the slot with a specific time and resource."""
        self.time = time
        self.resource = resource
        self.isAvailable = True

@dataclass
class State:
    description: str

    def transitionTo(self, new_state: Any) -> "State":
        """Transition to a new state."""
        if isinstance(new_state, State):
            return new_state
        if isinstance(new_state, str):
            return State(description=new_state)
        return State(description=str(new_state))

@dataclass
class Operation:
    initiator: Actor
    target: list[Resource]
    channel: list[Interface]
    grant: Permission
    pre: State
    post: State

    @staticmethod
    def create(initiator: Actor, resource: Resource, permission: Permission) -> "Operation":
        """Factory method to create an Operation."""
        if not isinstance(initiator, Actor):
            raise ValueError("initiator must be an Actor")
        if not isinstance(resource, Resource):
            raise ValueError("resource must be a Resource")
        if not isinstance(permission, Permission):
            raise ValueError("permission must be a Permission")
        pre_state = State(description="pre")
        post_state = State(description="post")
        return Operation(
            initiator=initiator,
            target=[resource],
            channel=[],
            grant=permission,
            pre=pre_state,
            post=post_state,
        )

@dataclass
class OperationSlot:
    op: Operation
    slot: Slot

    @staticmethod
    def create(operation: Operation, new_slot: Slot) -> "OperationSlot":
        """Factory method to create an OperationSlot."""
        if not isinstance(operation, Operation):
            raise ValueError("operation must be an Operation")
        if not isinstance(new_slot, Slot):
            raise ValueError("new_slot must be a Slot")
        return OperationSlot(op=operation, slot=new_slot)

@dataclass
class SlotId:
    pass

@dataclass
class SlotCreatedEvent:
    pass

@dataclass
class SlotUpdatedEvent:
    pass


@dataclass
class Interface:
    kind: str
    encrypted: bool
    authenticated: bool


def find_earliest_available_slot(
    existing_slots: list[Slot],
    reference_time: int = 0,
    slot_duration: int = SLOT_DURATION_MINUTES,
    gap: int = GAP_MINUTES,
) -> int:
    """Find the earliest available time slot respecting gaps.

    Args:
        existing_slots: List of existing allocated slots.
        reference_time: The reference time in minutes (0 = now).
        slot_duration: Duration of each slot in minutes (default 5).
        gap: Required gap between slots in minutes (default 3).

    Returns:
        The start time (in minutes) of the earliest available slot.
    """
    if not existing_slots:
        return reference_time

    sorted_slots = sorted(existing_slots, key=lambda s: s.time)

    first_slot_start = sorted_slots[0].time
    if reference_time + slot_duration + gap <= first_slot_start:
        return reference_time

    for i in range(len(sorted_slots) - 1):
        current_end = sorted_slots[i].time + slot_duration + gap
        next_start = sorted_slots[i + 1].time
        if current_end + slot_duration + gap <= next_start:
            return current_end

    last_end = sorted_slots[-1].time + slot_duration + gap
    return last_end
