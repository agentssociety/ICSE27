from __future__ import annotations

from typing import Optional, Protocol
from datetime import datetime, timedelta

from src.dto.slot.slot_dto import SlotCreateRequest, SlotUpdateRequest, SlotResponse
from src.repository.slot.slot_repository import SlotRepository
from src.domain.slot.Slot import Slot


class SlotService(Protocol):
    """Interface for slot-related business logic."""

    def allocate_slot(self, data: SlotCreateRequest) -> SlotResponse:
        """Allocate a new time slot with proper duration and gap validation."""
        ...

    def allocate_arrival_first(self, arrival_slot: SlotCreateRequest, departure_slot: SlotCreateRequest) -> list[SlotResponse]:
        """Allocate slots prioritizing arrivals over departures when both request the same time period."""
        ...

    def prioritize_emergency_flight(self, emergency_flight_data: SlotCreateRequest, existing_slots_filter: Optional[list[int]] = None) -> SlotResponse:
        """Assign an immediate slot for emergency flights and re-queue non-emergency flights."""
        ...

    def get_slot(self, slot_id: int) -> Optional[SlotResponse]:
        """Get a slot by its ID."""
        ...

    def get_all_slots(self, skip: int = 0, limit: int = 100) -> list[SlotResponse]:
        """List all slots with pagination."""
        ...

    def update_slot(self, slot_id: int, data: SlotUpdateRequest) -> Optional[SlotResponse]:
        """Update an existing slot."""
        ...

    def delete_slot(self, slot_id: int) -> bool:
        """Delete a slot by its ID."""
        ...


class SlotServiceImpl:
    """Concrete implementation of SlotService backed by a SlotRepository."""

    def __init__(self, repository: SlotRepository) -> None:
        if repository is None:
            raise ValueError("repository must not be None")
        self._repository = repository

    def allocate_slot(self, data: SlotCreateRequest) -> SlotResponse:
        if data.endTime <= data.startTime:
            raise ValueError("endTime must be after startTime")

        # Validate slot duration is 5 minutes
        actual_duration = data.endTime - data.startTime
        if actual_duration != timedelta(minutes=5):
            raise ValueError(f"Slot duration must be exactly 5 minutes, got {actual_duration}")

        # Check gaps with existing slots
        existing = self._repository.get_all_slots()
        slot = Slot(
            startTime=data.startTime,
            endTime=data.endTime,
        )
        # Verify adjacent gaps
        adjacent_ok = slot.checkAdjacentGap(slot, [Slot(
            startTime=SlotResponse.model_validate(s).startTime,
            endTime=SlotResponse.model_validate(s).endTime,
        ) for s in existing])
        if not adjacent_ok:
            raise ValueError("Adjacent gap of at least 3 minutes is required between slots")

        return self._repository.create(data)

    def allocate_arrival_first(self, arrival_slot: SlotCreateRequest, departure_slot: SlotCreateRequest) -> list[SlotResponse]:
        """Allocate slots prioritizing arrivals over departures when both request the same time period."""
        # Validate both slots
        if arrival_slot.endTime <= arrival_slot.startTime:
            raise ValueError("arrival_slot endTime must be after startTime")
        if departure_slot.endTime <= departure_slot.startTime:
            raise ValueError("departure_slot endTime must be after startTime")

        # Validate both are 5 minutes
        for name, s in [("arrival", arrival_slot), ("departure", departure_slot)]:
            actual = s.endTime - s.startTime
            if actual != timedelta(minutes=5):
                raise ValueError(f"{name} slot duration must be exactly 5 minutes, got {actual}")

        arrival_slot_with_type = SlotCreateRequest(
            startTime=arrival_slot.startTime,
            endTime=arrival_slot.endTime,
            flight_type="arrival",
            duration=arrival_slot.duration,
            gapAfter=arrival_slot.gapAfter,
        )
        departure_slot_with_type = SlotCreateRequest(
            startTime=departure_slot.startTime,
            endTime=departure_slot.endTime,
            flight_type="departure",
            duration=departure_slot.duration,
            gapAfter=departure_slot.gapAfter,
        )

        # Allocate arrival first (higher priority)
        arrival_result = self._repository.create(arrival_slot_with_type)

        # Then allocate departure slot if there's no conflict
        existing = self._repository.get_all_slots()
        dep_slot_obj = Slot(
            startTime=departure_slot.startTime,
            endTime=departure_slot.endTime,
        )
        if dep_slot_obj.checkOverlap(dep_slot_obj, [Slot(
            startTime=SlotResponse.model_validate(s).startTime,
            endTime=SlotResponse.model_validate(s).endTime,
        ) for s in existing]):
            return [arrival_result]

        departure_result = self._repository.create(departure_slot_with_type)
        return [arrival_result, departure_result]

    def get_slot(self, slot_id: int) -> Optional[SlotResponse]:
        if slot_id < 0:
            raise ValueError("slot_id must be non-negative")
        return self._repository.get_by_id(slot_id)

    def get_all_slots(self, skip: int = 0, limit: int = 100) -> list[SlotResponse]:
        if skip < 0:
            raise ValueError("skip must be non-negative")
        if limit < 1:
            raise ValueError("limit must be at least 1")
        return self._repository.get_all(skip=skip, limit=limit)

    def update_slot(self, slot_id: int, data: SlotUpdateRequest) -> Optional[SlotResponse]:
        if slot_id < 0:
            raise ValueError("slot_id must be non-negative")
        return self._repository.update(slot_id, data)

    def delete_slot(self, slot_id: int) -> bool:
        if slot_id < 0:
            raise ValueError("slot_id must be non-negative")
        return self._repository.delete(slot_id)
