from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.time_slot.time_slot_dto import TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse
from src.orm.time_slot.time_slot_orm import TimeSlotORM


class SQLAlchemyTimeSlotRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TimeSlotResponse]:
        row = self._session.get(TimeSlotORM, item_id)
        return TimeSlotResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TimeSlotResponse]:
        rows = self._session.query(TimeSlotORM).offset(skip).limit(limit).all()
        return [TimeSlotResponse.model_validate(r) for r in rows]

    def create(self, data: TimeSlotCreate) -> TimeSlotResponse:
        row = TimeSlotORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TimeSlotResponse.model_validate(row)

    def update(self, item_id: int, data: TimeSlotUpdate) -> Optional[TimeSlotResponse]:
        row = self._session.get(TimeSlotORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TimeSlotResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TimeSlotORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
