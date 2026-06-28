from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.orm.runway.runway_orm import RunwayORM
from src.orm.slot.slot_orm import SlotORM
from src.orm.flight.flight_orm import FlightORM
from src.api.runway.runway_router import get_runway_timetable
from src.dto.runway.runway_dto import RunwayTimetableResponse, TimetableEntry


class TestRunwayTimetable:
    def test_timetable_returns_slot_and_flights(self):
        """Test that timetable returns slot and flight entries for a valid runway."""
        mock_db = MagicMock(spec=Session)

        # Mock runway with a slot
        mock_runway = MagicMock(spec=RunwayORM)
        mock_runway.id = "RWY-01"
        mock_runway.configuration = "active"
        mock_slot = MagicMock(spec=SlotORM)
        mock_slot.id = 1
        mock_slot.time = 100
        mock_slot.isAvailable = True
        mock_runway.slot = mock_slot

        # Mock flights
        mock_flight1 = MagicMock(spec=FlightORM)
        mock_flight1.id = 1
        mock_flight1.flightNumber = "AA123"
        mock_flight1.aircraftType = "Boeing 737"

        mock_flight2 = MagicMock(spec=FlightORM)
        mock_flight2.id = 2
        mock_flight2.flightNumber = "BB456"
        mock_flight2.aircraftType = "Airbus A320"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_runway
        mock_db.query.return_value.all.return_value = [mock_flight1, mock_flight2]

        result = get_runway_timetable(runway_id="RWY-01", db=mock_db)

        assert isinstance(result, RunwayTimetableResponse)
        assert result.runway_id == "RWY-01"
        assert result.runway_status == "active"
        assert len(result.entries) == 3  # 1 slot + 2 flights

        # Verify slot entry
        slot_entry = result.entries[0]
        assert slot_entry.slot_id == 1
        assert slot_entry.slot_time == 100
        assert slot_entry.status == "allocated"

        # Verify flight entries
        flight_numbers = [e.flight_number for e in result.entries if e.flight_id is not None]
        assert "AA123" in flight_numbers
        assert "BB456" in flight_numbers

    def test_timetable_runway_not_found(self):
        """Test that 404 is raised for non-existent runway."""
        mock_db = MagicMock(spec=Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        from fastapi import HTTPException
        with pytest.raises(HTTPException) as excinfo:
            get_runway_timetable(runway_id="nonexistent", db=mock_db)
        assert excinfo.value.status_code == 404

    def test_timetable_no_slot(self):
        """Test timetable when runway has no slot."""
        mock_db = MagicMock(spec=Session)
        mock_runway = MagicMock(spec=RunwayORM)
        mock_runway.id = "RWY-02"
        mock_runway.configuration = "standby"
        mock_runway.slot = None
        mock_db.query.return_value.filter.return_value.first.return_value = mock_runway
        mock_db.query.return_value.all.return_value = []

        result = get_runway_timetable(runway_id="RWY-02", db=mock_db)
        assert len(result.entries) == 0

    def test_timetable_multiple_flights_no_slot(self):
        """Test timetable with multiple flights but no slot."""
        mock_db = MagicMock(spec=Session)
        mock_runway = MagicMock(spec=RunwayORM)
        mock_runway.id = "RWY-03"
        mock_runway.configuration = "active"
        mock_runway.slot = None
        mock_db.query.return_value.filter.return_value.first.return_value = mock_runway

        flights = []
        for i, (num, atype) in enumerate([("BA001", "Airbus A380"), ("LH002", "Boeing 747")]):
            f = MagicMock(spec=FlightORM)
            f.id = i + 1
            f.flightNumber = num
            f.aircraftType = atype
            flights.append(f)
        mock_db.query.return_value.all.return_value = flights

        result = get_runway_timetable(runway_id="RWY-03", db=mock_db)
        assert len(result.entries) == 2
        flight_numbers = [e.flight_number for e in result.entries]
        assert "BA001" in flight_numbers
        assert "LH002" in flight_numbers

    def test_timetable_with_slot_and_multiple_flights(self):
        """Test timetable with a slot and multiple flights."""
        mock_db = MagicMock(spec=Session)
        mock_runway = MagicMock(spec=RunwayORM)
        mock_runway.id = "RWY-04"
        mock_runway.configuration = "active"
        mock_slot = MagicMock(spec=SlotORM)
        mock_slot.id = 5
        mock_slot.time = 200
        mock_slot.isAvailable = False
        mock_runway.slot = mock_slot
        mock_db.query.return_value.filter.return_value.first.return_value = mock_runway

        flights = [
            MagicMock(spec=FlightORM, id=10, flightNumber="CA001", aircraftType="Cessna"),
            MagicMock(spec=FlightORM, id=11, flightNumber="DA002", aircraftType="Dash 8"),
        ]
        mock_db.query.return_value.all.return_value = flights

        result = get_runway_timetable(runway_id="RWY-04", db=mock_db)
        assert len(result.entries) == 3
        assert result.entries[0].status == "occupied"  # slot not available
        assert result.entries[0].slot_id == 5
        assert result.entries[0].slot_time == 200
