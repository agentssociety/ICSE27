from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.slot.slot_dto import SlotCreate, SlotUpdate, SlotResponse
from src.orm.slot.slot_orm import SlotORM


class SQLAlchemySlotRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SlotResponse]:
        row = self._session.get(SlotORM, item_id)
        return SlotResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SlotResponse]:
        rows = self._session.query(SlotORM).offset(skip).limit(limit).all()
        return [SlotResponse.model_validate(r) for r in rows]

    def create(self, data: SlotCreate) -> SlotResponse:
        row = SlotORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SlotResponse.model_validate(row)

    def update(self, item_id: int, data: SlotUpdate) -> Optional[SlotResponse]:
        row = self._session.get(SlotORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SlotResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SlotORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
