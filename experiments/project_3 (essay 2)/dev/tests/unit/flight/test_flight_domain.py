from __future__ import annotations

from datetime import datetime

import pytest

from src.domain.flight.Flight import (
    Flight,
    FlightType,
    FlightStatus,
    FlightId,
    FlightCreatedEvent,
    FlightUpdatedEvent,
    Resource,
    Permission,
    State,
)


class TestFlightDomain:
    def test_create_flight_with_valid_data(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="American Airlines",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        assert flight.flightNumber == "AA123"
        assert flight.airline == "American Airlines"
        assert flight.origin == "JFK"
        assert flight.destination == "LAX"
        assert flight.type == FlightType.ARRIVAL
        assert flight.status == FlightStatus.ACTIVE
        assert flight.note == ""

    def test_set_flight_number_valid(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        flight.setFlightNumber("BB456")
        assert flight.flightNumber == "BB456"

    def test_set_flight_number_invalid(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        with pytest.raises(ValueError):
            flight.setFlightNumber("")

    def test_set_type_valid(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        flight.setType(FlightType.DEPARTURE)
        assert flight.type == FlightType.DEPARTURE

    def test_set_type_invalid(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        with pytest.raises(TypeError):
            flight.setType("invalid")  # type: ignore[arg-type]

    def test_set_status(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        flight.setStatus(FlightStatus.CANCELLED)
        assert flight.status == FlightStatus.CANCELLED

    def test_set_status_invalid(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        with pytest.raises(TypeError):
            flight.setStatus("cancelled")  # type: ignore[arg-type]

    def test_cancel_flight(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        flight.cancel()
        assert flight.status == FlightStatus.CANCELLED

    def test_validate_new_schedule(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        assert flight.validateNewSchedule(datetime(2025, 6, 1, 12, 0, 0)) is True
        assert flight.validateNewSchedule(None) is False

    def test_get_status(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        assert flight.getStatus() == FlightStatus.ACTIVE

    def test_set_scheduled_time(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        new_time = datetime(2025, 6, 1, 14, 0, 0)
        flight.setScheduledTime(new_time)
        assert flight.scheduledTime == new_time

    def test_flight_id_generates_uuid(self) -> None:
        fid = FlightId()
        assert fid.value != ""

    def test_flight_type_enum(self) -> None:
        assert FlightType.ARRIVAL.value == "arrival"
        assert FlightType.DEPARTURE.value == "departure"

    def test_flight_status_enum(self) -> None:
        assert FlightStatus.ACTIVE.value == "active"
        assert FlightStatus.CANCELLED.value == "cancelled"

    def test_create_method(self) -> None:
        flight = Flight(
            flightNumber="AA123",
            airline="AA",
            origin="JFK",
            destination="LAX",
            scheduledTime=datetime(2025, 6, 1, 10, 0, 0),
            type=FlightType.ARRIVAL,
        )
        result = flight.create({
            "flightNumber": "BB456",
            "airline": "Delta",
            "origin": "ORD",
            "destination": "MIA",
            "scheduledTime": datetime(2025, 6, 2, 8, 0, 0),
            "type": FlightType.DEPARTURE,
        })
        assert result.flightNumber == "BB456"
        assert result.airline == "Delta"
        assert result.type == FlightType.DEPARTURE