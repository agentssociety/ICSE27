from __future__ import annotations

import pytest
from datetime import datetime

from src.domain.flight.Flight import Flight, Direction
from src.domain.slot.Slot import Slot
from src.service.flight.flight_service import FlightRegistrationServiceImpl


class TestFlightRegistrationService:
    def test_arrival_flights_get_priority(self) -> None:
        """Test that all arrival flights are allocated slots before departure flights."""
        service = FlightRegistrationServiceImpl()
        reference_time = 100  # 100 minutes after some reference
        
        arrivals = [
            Flight("ARR001", "Boeing 737", datetime(2024, 1, 15, 10, 0), Direction.INCOMING),
            Flight("ARR002", "Airbus A320", datetime(2024, 1, 15, 10, 5), Direction.INCOMING),
        ]
        departures = [
            Flight("DEP001", "Boeing 737", datetime(2024, 1, 15, 10, 10), Direction.OUTGOING),
        ]
        all_flights = arrivals + departures

        result = service.allocate_slot_with_priority(
            flights=all_flights, existing_slots=[], reference_time=reference_time
        )

        # All arrivals should have slots assigned
        assert "ARR001" in result
        assert "ARR002" in result
        # Departure should also have a slot
        assert "DEP001" in result

        # Arrivals should get earlier slots than departure
        assert result["ARR001"] < result["DEP001"]
        assert result["ARR002"] < result["DEP001"]

    def test_arrival_gets_slot_when_conflict_with_departure(self) -> None:
        """Test that when an arrival and departure compete for the same slot, the arrival wins."""
        service = FlightRegistrationServiceImpl()
        reference_time = 0

        # One departure already has a slot
        existing_slots = [Slot(time=0)]
        
        # An arrival flight comes along and needs a slot
        arrival = Flight("ARR001", "Boeing 737", datetime(2024, 1, 15, 10, 0), Direction.INCOMING)
        departure = Flight("DEP001", "Boeing 737", datetime(2024, 1, 15, 10, 5), Direction.OUTGOING)

        result = service.allocate_slot_with_priority(
            flights=[arrival, departure], existing_slots=existing_slots, reference_time=0
        )

        # The arrival should get the earliest available slot (8 = 0+5+3)
        assert result["ARR001"] == 8
        # The departure gets a later slot
        assert result["DEP001"] > result["ARR001"]

    def test_departure_reallocated_when_arrival_needs_its_slot(self) -> None:
        """Test that a departure flight is reallocated when an arrival needs its slot."""
        service = FlightRegistrationServiceImpl()
        reference_time = 0

        # A departure already has a slot at time 0
        existing_slots = [Slot(time=0)]
        
        # An arrival flight comes along
        arrival = Flight("ARR001", "Boeing 737", datetime(2024, 1, 15, 10, 0), Direction.INCOMING)
        # This departure is competing
        departure = Flight("DEP001", "Boeing 737", datetime(2024, 1, 15, 10, 5), Direction.OUTGOING)

        result = service.allocate_slot_with_priority(
            flights=[arrival, departure], existing_slots=existing_slots, reference_time=0
        )

        # The arrival gets the earliest slot
        earliest_slot = min(result.values())
        assert result["ARR001"] == earliest_slot
        # The departure gets a later slot
        assert result["DEP001"] > result["ARR001"]

    def test_both_arrivals_and_departures_get_slots(self) -> None:
        """Test that all flights get slots, with arrivals prioritized."""
        service = FlightRegistrationServiceImpl()
        reference_time = 0

        arrivals = [
            Flight("ARR1", "Boeing 737", datetime(2024, 1, 15, 10, 0), Direction.INCOMING),
            Flight("ARR2", "Airbus A320", datetime(2024, 1, 15, 10, 5), Direction.INCOMING),
        ]
        departures = [
            Flight("DEP1", "Boeing 737", datetime(2024, 1, 15, 10, 10), Direction.OUTGOING),
            Flight("DEP2", "Airbus A320", datetime(2024, 1, 15, 10, 15), Direction.OUTGOING),
        ]
        all_flights = arrivals + departures

        result = service.allocate_slot_with_priority(
            flights=all_flights, existing_slots=[], reference_time=0
        )

        # All flights should have slots
        assert len(result) == 4
        assert all(f.flightNumber in result for f in all_flights)

        # Arrival slots should be before departure slots
        arrival_times = [result[f.flightNumber] for f in arrivals]
        departure_times = [result[f.flightNumber] for f in departures]
        assert max(arrival_times) < min(departure_times)
