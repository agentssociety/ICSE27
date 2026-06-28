from __future__ import annotations

import pytest
from datetime import datetime

from src.domain.flight.Flight import Flight, Direction, AircraftMovementLog


class TestFlightDomain:
    def test_create_incoming_flight(self) -> None:
        """Test that an incoming flight can be created with required fields."""
        flight = Flight(
            flightNumber="AA123",
            aircraftType="Boeing 737",
            scheduledTime=datetime(2024, 1, 15, 14, 30),
            direction=Direction.INCOMING,
        )
        assert flight.flightNumber == "AA123"
        assert flight.aircraftType == "Boeing 737"
        assert flight.direction == Direction.INCOMING

    def test_create_outgoing_flight(self) -> None:
        """Test that an outgoing flight can be created."""
        flight = Flight(
            flightNumber="BB456",
            aircraftType="Airbus A320",
            scheduledTime=datetime(2024, 1, 15, 16, 0),
            direction=Direction.OUTGOING,
        )
        assert flight.flightNumber == "BB456"
        assert flight.direction == Direction.OUTGOING

    def test_aircraft_movement_log_add_entry(self) -> None:
        """Test that a flight appears in the aircraft movement log after registration."""
        log = AircraftMovementLog()
        flight = Flight(
            flightNumber="AA123",
            aircraftType="Boeing 737",
            scheduledTime=datetime(2024, 1, 15, 14, 30),
            direction=Direction.INCOMING,
        )
        log.add_entry(flight)
        entries = log.get_all_entries()
        assert len(entries) == 1
        assert entries[0].flightNumber == "AA123"

    def test_aircraft_movement_log_multiple_entries(self) -> None:
        """Test that multiple flights can be added to the log."""
        log = AircraftMovementLog()
        flight1 = Flight("AA123", "Boeing 737", datetime(2024, 1, 15, 14, 30), Direction.INCOMING)
        flight2 = Flight("BB456", "Airbus A320", datetime(2024, 1, 15, 16, 0), Direction.OUTGOING)
        log.add_entry(flight1)
        log.add_entry(flight2)
        assert len(log.get_all_entries()) == 2
