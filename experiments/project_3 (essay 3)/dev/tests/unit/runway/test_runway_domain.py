from __future__ import annotations

import pytest
from datetime import timedelta

from src.domain.runway.Runway import (
    Runway, RunwayId, RunwayCreatedEvent, RunwayUpdatedEvent,
    FlightSchedule, DelayCalculation, RunwayClosureRequest,
    Airport_Operations_Manager, Flight_Control_Center, Passenger_Services_Department,
    Permission, Actor, Resource, State, Pre1, Pre2, Post1, Post2, Post3
)


class TestRunwayDomain:
    """Tests for the Runway domain class."""

    def test_create_runway(self) -> None:
        runway = Runway(id="RW01", operatingHours="06:00-22:00")
        assert runway.id == "RW01"
        assert runway.operatingHours == "06:00-22:00"
        assert runway.is_closed is False
        assert len(runway.slots) == 0

    def test_close_runway(self) -> None:
        runway = Runway(id="RW01")
        assert runway.is_closed is False
        runway.close()
        assert runway.is_closed is True

    def test_open_runway(self) -> None:
        runway = Runway(id="RW01")
        runway.close()
        assert runway.is_closed is True
        runway.open()
        assert runway.is_closed is False

    def test_runway_id_creation(self) -> None:
        rid = RunwayId(id="RW01")
        assert rid.id == "RW01"

    def test_runway_created_event(self) -> None:
        event = RunwayCreatedEvent(runway_id="RW01")
        assert isinstance(event, RunwayCreatedEvent)

    def test_runway_updated_event(self) -> None:
        event = RunwayUpdatedEvent(runway_id="RW01")
        assert isinstance(event, RunwayUpdatedEvent)

    def test_flight_schedule_reassign(self) -> None:
        runway1 = Runway(id="RW01")
        runway2 = Runway(id="RW02")
        flight = type("Flight", (), {"id": "FL001", "runway": runway1})()
        schedule = FlightSchedule(flights=[flight])
        schedule.reassignFlights("RW01", [runway1, runway2])
        # After reassignment, flight should be on runway2
        assert flight.runway.id == "RW02"

    def test_flight_schedule_mark_delayed(self) -> None:
        flight = type("Flight", (), {"id": "FL001", "delayed": False})()
        schedule = FlightSchedule(flights=[flight])
        schedule.markFlightDelayed("FL001", timedelta(minutes=30))
        assert flight.delayed is True

    def test_delay_calculation(self) -> None:
        calc = DelayCalculation()
        flight = type("Flight", (), {"estimatedDepartureTime": "2025-06-15T10:00:00Z"})()
        delay = calc.calculateDelay(flight)
        assert isinstance(delay, timedelta)

    def test_airport_ops_manager(self) -> None:
        aom = Airport_Operations_Manager()
        assert aom.name == "AOM"

    def test_flight_control_center(self) -> None:
        fcc = Flight_Control_Center()
        assert fcc.name == "FCC"

    def test_passenger_services(self) -> None:
        psd = Passenger_Services_Department()
        assert psd.name == "PSD"

    def test_runway_closure_request(self) -> None:
        req = RunwayClosureRequest(runway_id="RW01", reason="Maintenance")
        assert req.runway_id == "RW01"
        assert req.reason == "Maintenance"

    def test_state_transition(self) -> None:
        s1 = State(name="initial")
        s2 = State(name="final")
        s1.transitionTo(s2)
        assert s1.name == "final"
