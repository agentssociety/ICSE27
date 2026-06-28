from __future__ import annotations

from typing import Any, Protocol

from src.domain.slot.Slot import Slot, find_earliest_available_slot, SLOT_DURATION_MINUTES, GAP_MINUTES

"""
Service layer for the Slot domain class

Package: service.slot
Layer: service
Related tasks: #47, #48, #49, #50, #51, #52
Requirement coverage:
- Automate Earliest Available Time Slot Allocation with Gap
- Priority Slot Allocation for Arrival Flights
- Prevent Overlapping Flight Assignments
- Automatic Reassignment of Flights During Runway Closure
- Handle Emergency Flights
"""

class SlotService(Protocol):
    def allocate_slot(self, existing_slots: list[Slot], reference_time: int = 0) -> int:
        ...

class SlotServiceImpl:
    def __init__(self) -> None:
        pass

    def allocate_slot(self, existing_slots: list[Slot], reference_time: int = 0) -> int:
        """Allocate the earliest available 5-minute slot respecting 3-minute gaps."""
        return find_earliest_available_slot(
            existing_slots=existing_slots,
            reference_time=reference_time,
            slot_duration=SLOT_DURATION_MINUTES,
            gap=GAP_MINUTES,
        )
