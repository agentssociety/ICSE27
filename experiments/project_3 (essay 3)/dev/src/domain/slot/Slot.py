from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

"""
Domain layer for the Slot domain class

Package: domain.slot
Layer: domain
Related tasks: #73, #74, #75, #76, #77, #78
Requirement coverage:
- Allocate 5-minute slots with a 3-minute gap between successive slots
- Prioritize Arrivals Over Departures When Allocating Slots
- Detect and Prevent Slot Overlaps
- Runway Closure and Flight Reassignment Management
- Prioritize Emergency Flights and Re-queue Non-Emergency Flights
"""


class FlightType(Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class Slot:
    """A time slot allocated for a flight on a runway."""

    def __init__(
        self,
        startTime: datetime,
        endTime: datetime,
        flight: Any = None,
        runway: Any = None,
        flight_type: FlightType = FlightType.ARRIVAL,
        duration: timedelta = timedelta(minutes=5),
        gapAfter: timedelta = timedelta(minutes=3),
    ) -> None:
        self.startTime = startTime
        self.endTime = endTime
        self.flight = flight
        self.runway = runway
        self.flight_type = flight_type
        self.duration = duration
        self.gapAfter = gapAfter

    def checkOverlap(self, newSlot: Slot, existingSlots: list[Slot]) -> bool:
        """Check if newSlot overlaps with any existing slot."""
        for existing in existingSlots:
            if newSlot.startTime < existing.endTime and newSlot.endTime > existing.startTime:
                return True  # overlap detected
        return False

    def checkAdjacentGap(self, newSlot: Slot, existingSlots: list[Slot]) -> bool:
        """Check that there is at least a 3-minute gap before the new slot
        and after the new slot relative to existing adjacent slots."""
        for existing in existingSlots:
            # If new slot is after existing slot, check gap
            if newSlot.startTime >= existing.endTime:
                gap = newSlot.startTime - existing.endTime
                if gap < timedelta(minutes=3):
                    return False
            # If new slot is before existing slot, check gap the other way
            if newSlot.endTime <= existing.startTime:
                gap = existing.startTime - newSlot.endTime
                if gap < timedelta(minutes=3):
                    return False
        return True

    def create(
        self,
        startTime: datetime,
        endTime: datetime,
        nduration_5: timedelta = timedelta(minutes=5),
        gapAfter_3: timedelta = timedelta(minutes=3),
    ) -> Slot:
        """Factory method to create a new Slot with validation."""
        if endTime <= startTime:
            raise ValueError("endTime must be after startTime")
        if nduration_5 != timedelta(minutes=5):
            raise ValueError("Slot duration must be exactly 5 minutes")
        if gapAfter_3 != timedelta(minutes=3):
            raise ValueError("Gap after slot must be exactly 3 minutes")
        # Verify the actual duration matches
        actual_duration = endTime - startTime
        if actual_duration != nduration_5:
            raise ValueError("Slot duration must be exactly 5 minutes")
        return Slot(
            startTime=startTime,
            endTime=endTime,
            duration=nduration_5,
            gapAfter=gapAfter_3,
        )

    def verifyAllocations(self, allSlots: list[Slot]) -> bool:
        """Verify that every slot in the list satisfies the constraints
        (5-minute duration, 3-minute gap between slots)."""
        if not allSlots:
            return True
        for i, slot in enumerate(allSlots):
            # Check each slot duration is 5 minutes
            expected_end = slot.startTime + timedelta(minutes=5)
            if slot.endTime != expected_end:
                return False
            # Check gap between consecutive slots
            if i > 0:
                prev_slot = allSlots[i - 1]
                gap = slot.startTime - prev_slot.endTime
                if gap < timedelta(minutes=3):
                    return False
        return True


@dataclass
class Actor:
    name: str
    permissions: list[Permission]


@dataclass
class Resource:
    owner: Actor
    accessible: list[Actor]

    def isAccessible(self, actor: Actor) -> bool:
        return actor in self.accessible or actor == self.owner


@dataclass
class Operation:
    pass

    def create(self, actor: Any, resource: Any, slot: Any) -> None:
        pass


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PREIDLE = "preidle"
    POST1 = "post1"
    POST2 = "post2"


@dataclass
class SlotId:
    pass


@dataclass
class SlotCreatedEvent:
    pass


@dataclass
class SlotUpdatedEvent:
    pass
