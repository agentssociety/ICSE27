from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.failed_attempt.failed_attempt_dto import FailedAttemptCreate, FailedAttemptUpdate, FailedAttemptResponse
from src.orm.failed_attempt.failed_attempt_orm import FailedAttemptORM


class SQLAlchemyFailedAttemptRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[FailedAttemptResponse]:
        row = self._session.get(FailedAttemptORM, item_id)
        return FailedAttemptResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FailedAttemptResponse]:
        rows = self._session.query(FailedAttemptORM).offset(skip).limit(limit).all()
        return [FailedAttemptResponse.model_validate(r) for r in rows]

    def create(self, data: FailedAttemptCreate) -> FailedAttemptResponse:
        row = FailedAttemptORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return FailedAttemptResponse.model_validate(row)

    def update(self, item_id: int, data: FailedAttemptUpdate) -> Optional[FailedAttemptResponse]:
        row = self._session.get(FailedAttemptORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return FailedAttemptResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(FailedAttemptORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
