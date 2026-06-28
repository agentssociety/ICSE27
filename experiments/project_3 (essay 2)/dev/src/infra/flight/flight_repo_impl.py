from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.dto.flight.flight_dto import FlightRegistrationRequest, FlightUpdateRequest
from src.orm.flight.flight_orm import FlightORM


class SQLAlchemyFlightRepository:
    """Repository implementation for Flight entity using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[FlightORM]:
        return self._session.get(FlightORM, item_id)

    def get_by_flight_number(self, fn: str) -> Optional[FlightORM]:
        return self._session.query(FlightORM).filter(
            FlightORM.flightNumber == fn
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FlightORM]:
        return self._session.query(FlightORM).offset(skip).limit(limit).all()

    def create(self, data: FlightRegistrationRequest) -> FlightORM:
        row = FlightORM(
            flightNumber=data.flightNumber,
            airline=data.airline,
            origin=data.origin,
            destination=data.destination,
            scheduledTime=data.scheduledTime,
            type=data.type,
            note=data.note or "",
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def update(self, item_id: int, data: FlightUpdateRequest) -> Optional[FlightORM]:
        row = self._session.get(FlightORM, item_id)
        if row is None:
            return None
        if data.flightNumber is not None:
            row.flightNumber = data.flightNumber
        if data.scheduledTime is not None:
            row.scheduledTime = data.scheduledTime
        self._session.commit()
        self._session.refresh(row)
        return row

    def delete(self, item_id: int) -> bool:
        row = self._session.get(FlightORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True

    def save(self, flight: FlightORM) -> FlightORM:
        self._session.add(flight)
        self._session.commit()
        self._session.refresh(flight)
        return flight

    def findByFlightNumber(self, fn: str) -> Optional[FlightORM]:
        return self.get_by_flight_number(fn)

    def update_by_flight_number(self, fn: str, data: FlightUpdateRequest) -> Optional[FlightORM]:
        row = self._session.query(FlightORM).filter(FlightORM.flightNumber == fn).first()
        if row is None:
            return None
        if data.scheduledTime is not None:
            row.scheduledTime = data.scheduledTime
        self._session.commit()
        self._session.refresh(row)
        return row