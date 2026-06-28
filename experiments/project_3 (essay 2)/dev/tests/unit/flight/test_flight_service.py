from __future__ import annotations

import pytest

from src.domain.flight.Flight import Flight, FlightType, FlightStatus
from datetime import datetime


class TestFlightService:
    def test_flight_registration(self) -> None:
        """Verify a flight can be registered with required fields."""
        flight = Flight(
            flightNumber="AA100",
            airline="American Airlines",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        assert flight.flightNumber == "AA100"
        assert flight.status == FlightStatus.ACTIVE

    def test_flight_can_be_cancelled(self) -> None:
        """Verify a flight can be cancelled."""
        flight = Flight(
            flightNumber="AA100",
            airline="AA",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        flight.cancel()
        assert flight.status == FlightStatus.CANCELLED

    def test_flight_can_be_edited(self) -> None:
        """Verify a flight can have its schedule updated."""
        flight = Flight(
            flightNumber="AA100",
            airline="AA",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        new_time = datetime(2025, 7, 1, 10, 0, 0)
        flight.setScheduledTime(new_time)
        assert flight.scheduledTime == new_time

class TestSlotAllocation:
    """Tests for the 5-minute slot allocation with 3-minute gaps."""

    def test_allocate_single_flight_slot(self) -> None:
        from datetime import datetime
        from src.domain.flight.Flight import Flight, FlightType, FlightStatus
        from src.service.flight.flight_service import allocate_slots, SLOT_DURATION_MINUTES

        flight = Flight(
            flightNumber="AA100",
            airline="AA",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        slots = allocate_slots([flight])
        slot_start, slot_end = slots["AA100"]
        assert slot_start == datetime(2025, 7, 1, 8, 0, 0)
        assert (slot_end - slot_start).seconds / 60 == SLOT_DURATION_MINUTES

    def test_three_minute_gap_between_slots(self) -> None:
        from datetime import datetime, timedelta
        from src.domain.flight.Flight import Flight, FlightType, FlightStatus
        from src.service.flight.flight_service import allocate_slots, SLOT_DURATION_MINUTES, GAP_MINUTES

        flight1 = Flight(
            flightNumber="AA100",
            airline="AA",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        flight2 = Flight(
            flightNumber="BB200",
            airline="BA",
            origin="LHR",
            destination="JFK",
            scheduledTime=datetime(2025, 7, 1, 8, 5, 0),
            type=FlightType.ARRIVAL,
        )
        slots = allocate_slots([flight1, flight2])
        _, end1 = slots["AA100"]
        start2, _ = slots["BB200"]
        gap = (start2 - end1).total_seconds() / 60
        assert gap >= GAP_MINUTES, f"Expected at least {GAP_MINUTES}min gap, got {gap}min"

    def test_each_flight_gets_five_minute_slot(self) -> None:
        from datetime import datetime
        from src.domain.flight.Flight import Flight, FlightType, FlightStatus
        from src.service.flight.flight_service import allocate_slots, SLOT_DURATION_MINUTES

        flights = [
            Flight(
                flightNumber=f"FL{i}",
                airline="AA",
                origin="JFK",
                destination="LHR",
                scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
                type=FlightType.DEPARTURE,
            )
            for i in range(3)
        ]
        slots = allocate_slots(flights)
        for fn, (start, end) in slots.items():
            duration = (end - start).total_seconds() / 60
            assert duration == SLOT_DURATION_MINUTES, f"{fn}: expected 5min slot, got {duration}min"


class TestArrivalPriority:
    """Tests for arrival prioritization over departures in slot allocation."""

    def test_arrival_gets_conflicting_slot(self) -> None:
        from datetime import datetime, timedelta
        from src.domain.flight.Flight import Flight, FlightType, FlightStatus
        from src.service.flight.flight_service import allocate_slots

        # Arrival and departure at same time - arrival should get the slot
        arrival = Flight(
            flightNumber="AA100",
            airline="AA",
            origin="LHR",
            destination="JFK",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.ARRIVAL,
        )
        departure = Flight(
            flightNumber="BB200",
            airline="BA",
            origin="JFK",
            destination="LHR",
            scheduledTime=datetime(2025, 7, 1, 8, 0, 0),
            type=FlightType.DEPARTURE,
        )
        slots = allocate_slots([departure, arrival])  # departure first in list
        arrival_start, _ = slots["AA100"]
        departure_start, _ = slots["BB200"]
        # Arrival should be first since it has priority for same time
        assert arrival_start <= departure_start

    def test_all_arrivals_before_departures(self) -> None:
        from datetime import datetime
        from src.domain.flight.Flight import Flight, FlightType, FlightStatus
        from src.service.flight.flight_service import allocate_slots

        flights = [
            Flight("D1", "AA", "JFK", "LHR", datetime(2025, 7, 1, 8, 0, 0), FlightType.DEPARTURE),
            Flight("A1", "BA", "LHR", "JFK", datetime(2025, 7, 1, 8, 0, 0), FlightType.ARRIVAL),
            Flight("D2", "UA", "JFK", "ORD", datetime(2025, 7, 1, 8, 5, 0), FlightType.DEPARTURE),
            Flight("A2", "LH", "FRA", "JFK", datetime(2025, 7, 1, 8, 5, 0), FlightType.ARRIVAL),
        ]
        slots = allocate_slots(flights)
        times = {fn: start for fn, (start, _) in slots.items()}
        # All arrivals should be scheduled before any departures that conflict
        assert times["A1"] <= times["D1"], "Arrival should be before or at same time as departure"
        assert times["A2"] <= times["D2"], "Arrival should be before or at same time as departure"
