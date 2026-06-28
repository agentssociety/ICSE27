from __future__ import annotations

import pytest
from datetime import datetime

from src.domain.flight.Flight import Flight, FlightId, FlightCreatedEvent, FlightUpdatedEvent


class TestFlightDomain:
    """Tests for the Flight domain class."""

    def test_create_flight(self) -> None:
        flight = Flight(
            flightNumber="BA123",
            origin="LHR",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        assert flight.flightNumber == "BA123"
        assert flight.origin == "LHR"
        assert flight.destination == "JFK"
        assert flight.estimatedDepartureTime == "2025-06-15T10:00:00Z"

    def test_flight_id_creation(self) -> None:
        fid = FlightId()
        assert isinstance(fid, FlightId)

    def test_flight_created_event(self) -> None:
        event = FlightCreatedEvent()
        assert isinstance(event, FlightCreatedEvent)

    def test_flight_updated_event(self) -> None:
        event = FlightUpdatedEvent()
        assert isinstance(event, FlightUpdatedEvent)
