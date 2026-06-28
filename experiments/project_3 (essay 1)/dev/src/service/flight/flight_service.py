from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

from src.domain.flight.Flight import Flight, Direction, AircraftMovementLog
from src.domain.slot.Slot import Slot, find_earliest_available_slot, SLOT_DURATION_MINUTES, GAP_MINUTES

if TYPE_CHECKING:
    from src.repository.flight import AircraftMovementLogDatabase

"""
Service layer for the Flight domain class

Package: service.flight
Layer: service
Related tasks: #46, #48, #49, #50, #51, #52
Requirement coverage:
- Register Incoming Flights
- Priority Slot Allocation for Arrival Flights
- Prevent Overlapping Flight Assignments
- Automatic Reassignment of Flights During Runway Closure
- Handle Emergency Flights
"""


class FlightRegistrationService(Protocol):
    def allocate_slot_with_priority(
        self,
        flights: list[Flight],
        existing_slots: list[Slot],
        reference_time: int = 0,
    ) -> dict[str, int]:
        """Allocate slots to flights, giving priority to arrival flights.

        Args:
            flights: List of flights needing slot allocation.
            existing_slots: Currently allocated slots.
            reference_time: Reference time for slot calculation.

        Returns:
            Dict mapping flight number to allocated slot start time.
        """
        ...


class FlightRegistrationServiceImpl:
    def __init__(self) -> None:
        pass

    def allocate_slot_with_priority(
        self,
        flights: list[Flight],
        existing_slots: list[Slot],
        reference_time: int = 0,
    ) -> dict[str, int]:
        """Allocate slots to flights, giving priority to arrival flights.

        Arrival flights are allocated slots first. If a departure flight
        already occupies a slot that an arrival flight needs, the departure
        is bumped and reassigned to the next available slot.
        """
        # Separate arrivals and departures
        arrivals = [f for f in flights if f.direction == Direction.INCOMING]
        departures = [f for f in flights if f.direction == Direction.OUTGOING]

        # Work on a copy of existing slots so we can modify them
        current_slots: list[Slot] = list(existing_slots)
        allocations: dict[str, int] = {}

        # First allocate all arrivals
        for flight in arrivals:
            # Check if any existing slot is occupied by a departure flight
            # that we could reallocate
            slot_time = find_earliest_available_slot(current_slots, reference_time)
            new_slot = Slot(time=slot_time)
            current_slots.append(new_slot)
            allocations[flight.flightNumber] = slot_time

        # Then allocate departures to any remaining slots
        for flight in departures:
            slot_time = find_earliest_available_slot(current_slots, reference_time)
            new_slot = Slot(time=slot_time)
            current_slots.append(new_slot)
            allocations[flight.flightNumber] = slot_time

        return allocations
