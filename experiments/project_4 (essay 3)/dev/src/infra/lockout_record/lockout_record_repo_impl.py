from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.lockout_record.lockout_record_dto import LockoutRecordCreate, LockoutRecordUpdate, LockoutRecordResponse
from src.orm.lockout_record.lockout_record_orm import LockoutRecordORM


class SQLAlchemyLockoutRecordRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[LockoutRecordResponse]:
        row = self._session.get(LockoutRecordORM, item_id)
        return LockoutRecordResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LockoutRecordResponse]:
        rows = self._session.query(LockoutRecordORM).offset(skip).limit(limit).all()
        return [LockoutRecordResponse.model_validate(r) for r in rows]

    def create(self, data: LockoutRecordCreate) -> LockoutRecordResponse:
        row = LockoutRecordORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return LockoutRecordResponse.model_validate(row)

    def update(self, item_id: int, data: LockoutRecordUpdate) -> Optional[LockoutRecordResponse]:
        row = self._session.get(LockoutRecordORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return LockoutRecordResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(LockoutRecordORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
