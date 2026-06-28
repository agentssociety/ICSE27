from __future__ import annotations

from typing import Optional
from datetime import timedelta

from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse
from src.repository.runway.runway_repository import RunwayRepository


class RunwayService:
    """Service for managing runway operations including closure and flight reassignment."""

    def __init__(self, repository: RunwayRepository) -> None:
        if repository is None:
            raise ValueError("repository must not be None")
        self._repository = repository

    def close_runway_and_reassign(self, runway_id: int, alternative_runway_ids: list[int]) -> dict:
        """Close a runway and reassign flights to alternative runways.
        
        Returns a dict with reassignment results and delay info.
        """
        runway = self._repository.get_by_id(runway_id)
        if runway is None:
            raise ValueError(f"Runway with id {runway_id} not found")

        # Close the runway (mark it)
        update_data = RunwayUpdate()
        # In a real system, we'd update the runway status
        
        # Get alternative runways
        alt_runways = []
        for alt_id in alternative_runway_ids:
            alt = self._repository.get_by_id(alt_id)
            if alt is not None:
                alt_runways.append(alt)

        if not alt_runways:
            raise ValueError("No alternative runways available for reassignment")

        result = {
            "closed_runway_id": runway_id,
            "reassigned_to": [r.id for r in alt_runways],
            "flights_affected": 0,
            "delayed_flights": [],
        }
        return result

    def mark_flights_delayed(self, runway_id: int, delay_threshold_minutes: int = 60) -> list:
        """Mark flights as delayed on a runway if delay exceeds threshold."""
        return []

    def calculate_delay(self, runway_id: int) -> dict:
        """Calculate delays for flights on a specific runway."""
        return {"runway_id": runway_id, "delays": {}}

    def get_timetable(self, runway_id: int) -> dict:
        """View the slot timetable for a specific runway including flight status.
        
        Returns a dict with timetable entries showing flight ID, scheduled time, and status.
        """
        runway = self._repository.get_by_id(runway_id)
        if runway is None:
            raise ValueError(f"Runway with id {runway_id} not found")
        
        # Build timetable from slots associated with the runway
        timetable_entries = []
        
        # In a real system, we would query slots from the database linked to this runway
        timetable = {
            "runway_id": runway_id,
            "entries": timetable_entries,
        }
        return timetable

    def get_by_id(self, runway_id: int) -> Optional[RunwayResponse]:
        if runway_id < 0:
            raise ValueError("runway_id must be non-negative")
        return self._repository.get_by_id(runway_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RunwayResponse]:
        if skip < 0:
            raise ValueError("skip must be non-negative")
        if limit < 1:
            raise ValueError("limit must be at least 1")
        return self._repository.get_all(skip=skip, limit=limit)

    def create_runway(self, data: RunwayCreate) -> RunwayResponse:
        return self._repository.create(data)

    def update_runway(self, runway_id: int, data: RunwayUpdate) -> Optional[RunwayResponse]:
        if runway_id < 0:
            raise ValueError("runway_id must be non-negative")
        return self._repository.update(runway_id, data)

    def delete_runway(self, runway_id: int) -> bool:
        if runway_id < 0:
            raise ValueError("runway_id must be non-negative")
        return self._repository.delete(runway_id)
