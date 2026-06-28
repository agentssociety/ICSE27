from __future__ import annotations

import pytest
from typing import Optional

from src.dto.flight.flight_dto import FlightCreate, FlightUpdate, FlightResponse
from src.repository.flight.flight_repository import FlightRepository
from src.service.flight.flight_service import FlightServiceImpl, FlightService


class FakeFlightRepository:
    """In-memory repository for testing."""
    
    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def get_by_id(self, item_id: int) -> Optional[FlightResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        return FlightResponse(**row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FlightResponse]:
        items = list(self._store.values())
        return [FlightResponse(**r) for r in items[skip:skip + limit]]

    def create(self, data: FlightCreate) -> FlightResponse:
        row_id = self._next_id
        self._next_id += 1
        row = {
            "id": row_id,
            "flightNumber": data.flightNumber,
            "origin": data.origin,
            "destination": data.destination,
            "estimatedDepartureTime": data.estimatedDepartureTime,
        }
        self._store[row_id] = row
        return FlightResponse(**row)

    def update(self, item_id: int, data: FlightUpdate) -> Optional[FlightResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                row[key] = value
        self._store[item_id] = row
        return FlightResponse(**row)

    def delete(self, item_id: int) -> bool:
        if item_id in self._store:
            del self._store[item_id]
            return True
        return False


class TestFlightServiceImpl:
    """Tests for FlightServiceImpl."""

    def setup_method(self) -> None:
        self.repo = FakeFlightRepository()
        self.service: FlightService = FlightServiceImpl(repository=self.repo)

    def test_register_flight_success(self) -> None:
        data = FlightCreate(
            flightNumber="BA123",
            origin="LHR",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        result = self.service.register_flight(data)
        assert result.id == 1
        assert result.flightNumber == "BA123"

    def test_register_flight_empty_number(self) -> None:
        data = FlightCreate(
            flightNumber="",
            origin="LHR",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        with pytest.raises(ValueError, match="flightNumber must not be empty"):
            self.service.register_flight(data)

    def test_register_flight_empty_origin(self) -> None:
        data = FlightCreate(
            flightNumber="BA123",
            origin="",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        with pytest.raises(ValueError, match="origin must not be empty"):
            self.service.register_flight(data)

    def test_get_flight_found(self) -> None:
        data = FlightCreate(
            flightNumber="BA123",
            origin="LHR",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        created = self.service.register_flight(data)
        result = self.service.get_flight(created.id)
        assert result is not None
        assert result.flightNumber == "BA123"

    def test_get_flight_not_found(self) -> None:
        result = self.service.get_flight(999)
        assert result is None

    def test_get_flight_negative_id(self) -> None:
        with pytest.raises(ValueError, match="flight_id must be non-negative"):
            self.service.get_flight(-1)

    def test_get_all_flights(self) -> None:
        data1 = FlightCreate(flightNumber="BA1", origin="A", destination="B", estimatedDepartureTime="T1")
        data2 = FlightCreate(flightNumber="BA2", origin="C", destination="D", estimatedDepartureTime="T2")
        self.service.register_flight(data1)
        self.service.register_flight(data2)
        results = self.service.get_all_flights()
        assert len(results) == 2

    def test_get_all_flights_with_skip_limit(self) -> None:
        for i in range(5):
            data = FlightCreate(
                flightNumber=f"BA{i}", origin="A", destination="B", estimatedDepartureTime=f"T{i}"
            )
            self.service.register_flight(data)
        results = self.service.get_all_flights(skip=2, limit=2)
        assert len(results) == 2

    def test_get_all_flights_negative_skip(self) -> None:
        with pytest.raises(ValueError, match="skip must be non-negative"):
            self.service.get_all_flights(skip=-1)

    def test_get_all_flights_zero_limit(self) -> None:
        with pytest.raises(ValueError, match="limit must be at least 1"):
            self.service.get_all_flights(limit=0)

    def test_update_flight(self) -> None:
        data = FlightCreate(
            flightNumber="BA123", origin="LHR", destination="JFK", estimatedDepartureTime="2025-06-15T10:00:00Z"
        )
        created = self.service.register_flight(data)
        update_data = FlightUpdate(destination="LAX")
        result = self.service.update_flight(created.id, update_data)
        assert result is not None
        assert result.destination == "LAX"
        assert result.flightNumber == "BA123"  # unchanged

    def test_update_flight_not_found(self) -> None:
        update_data = FlightUpdate(destination="LAX")
        result = self.service.update_flight(999, update_data)
        assert result is None

    def test_delete_flight(self) -> None:
        data = FlightCreate(
            flightNumber="BA123", origin="LHR", destination="JFK", estimatedDepartureTime="2025-06-15T10:00:00Z"
        )
        created = self.service.register_flight(data)
        deleted = self.service.delete_flight(created.id)
        assert deleted is True
        assert self.service.get_flight(created.id) is None

    def test_delete_flight_not_found(self) -> None:
        result = self.service.delete_flight(999)
        assert result is False

    def test_constructor_none_repo(self) -> None:
        with pytest.raises(ValueError, match="repository must not be None"):
            FlightServiceImpl(repository=None)
