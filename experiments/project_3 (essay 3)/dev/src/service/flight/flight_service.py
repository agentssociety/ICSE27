from __future__ import annotations

from typing import Optional, Protocol

from src.dto.flight.flight_dto import FlightCreate, FlightUpdate, FlightResponse
from src.repository.flight.flight_repository import FlightRepository


class FlightService(Protocol):
    """Interface for flight-related business logic."""

    def register_flight(self, data: FlightCreate) -> FlightResponse:
        """Register a new flight with estimated departure time."""
        ...

    def get_flight(self, flight_id: int) -> Optional[FlightResponse]:
        """Get a flight by its ID."""
        ...

    def get_all_flights(self, skip: int = 0, limit: int = 100) -> list[FlightResponse]:
        """List all flights with pagination."""
        ...

    def update_flight(self, flight_id: int, data: FlightUpdate) -> Optional[FlightResponse]:
        """Update an existing flight's details."""
        ...

    def delete_flight(self, flight_id: int) -> bool:
        """Delete a flight by its ID."""
        ...


class FlightServiceImpl:
    """Concrete implementation of FlightService backed by a FlightRepository."""

    def __init__(self, repository: FlightRepository) -> None:
        if repository is None:
            raise ValueError("repository must not be None")
        self._repository = repository

    def register_flight(self, data: FlightCreate) -> FlightResponse:
        if not data.flightNumber:
            raise ValueError("flightNumber must not be empty")
        if not data.origin:
            raise ValueError("origin must not be empty")
        if not data.destination:
            raise ValueError("destination must not be empty")
        if not data.estimatedDepartureTime:
            raise ValueError("estimatedDepartureTime must not be empty")
        return self._repository.create(data)

    def get_flight(self, flight_id: int) -> Optional[FlightResponse]:
        if flight_id < 0:
            raise ValueError("flight_id must be non-negative")
        return self._repository.get_by_id(flight_id)

    def get_all_flights(self, skip: int = 0, limit: int = 100) -> list[FlightResponse]:
        if skip < 0:
            raise ValueError("skip must be non-negative")
        if limit < 1:
            raise ValueError("limit must be at least 1")
        return self._repository.get_all(skip=skip, limit=limit)

    def update_flight(self, flight_id: int, data: FlightUpdate) -> Optional[FlightResponse]:
        if flight_id < 0:
            raise ValueError("flight_id must be non-negative")
        return self._repository.update(flight_id, data)

    def delete_flight(self, flight_id: int) -> bool:
        if flight_id < 0:
            raise ValueError("flight_id must be non-negative")
        return self._repository.delete(flight_id)
