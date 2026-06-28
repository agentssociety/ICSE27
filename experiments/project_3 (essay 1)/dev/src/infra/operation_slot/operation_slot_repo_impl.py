from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.operation_slot.operation_slot_dto import OperationSlotCreate, OperationSlotUpdate, OperationSlotResponse
from src.orm.operation_slot.operation_slot_orm import OperationSlotORM


class SQLAlchemyOperationSlotRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[OperationSlotResponse]:
        row = self._session.get(OperationSlotORM, item_id)
        return OperationSlotResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[OperationSlotResponse]:
        rows = self._session.query(OperationSlotORM).offset(skip).limit(limit).all()
        return [OperationSlotResponse.model_validate(r) for r in rows]

    def create(self, data: OperationSlotCreate) -> OperationSlotResponse:
        row = OperationSlotORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return OperationSlotResponse.model_validate(row)

    def update(self, item_id: int, data: OperationSlotUpdate) -> Optional[OperationSlotResponse]:
        row = self._session.get(OperationSlotORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return OperationSlotResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(OperationSlotORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
