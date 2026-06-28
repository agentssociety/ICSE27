from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.emergency_flight.emergency_flight_dto import EmergencyFlightCreate, EmergencyFlightUpdate, EmergencyFlightResponse
from src.orm.emergency_flight.emergency_flight_orm import EmergencyFlightORM


class SQLAlchemyEmergencyFlightRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[EmergencyFlightResponse]:
        row = self._session.get(EmergencyFlightORM, item_id)
        return EmergencyFlightResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[EmergencyFlightResponse]:
        rows = self._session.query(EmergencyFlightORM).offset(skip).limit(limit).all()
        return [EmergencyFlightResponse.model_validate(r) for r in rows]

    def create(self, data: EmergencyFlightCreate) -> EmergencyFlightResponse:
        row = EmergencyFlightORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return EmergencyFlightResponse.model_validate(row)

    def update(self, item_id: int, data: EmergencyFlightUpdate) -> Optional[EmergencyFlightResponse]:
        row = self._session.get(EmergencyFlightORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return EmergencyFlightResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(EmergencyFlightORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
