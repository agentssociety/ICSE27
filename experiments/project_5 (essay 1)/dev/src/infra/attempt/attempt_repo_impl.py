from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.attempt.attempt_dto import AttemptCreate, AttemptUpdate, AttemptResponse
from src.orm.attempt.attempt_orm import AttemptORM


class SQLAlchemyAttemptRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AttemptResponse]:
        row = self._session.get(AttemptORM, item_id)
        return AttemptResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AttemptResponse]:
        rows = self._session.query(AttemptORM).offset(skip).limit(limit).all()
        return [AttemptResponse.model_validate(r) for r in rows]

    def create(self, data: AttemptCreate) -> AttemptResponse:
        row = AttemptORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AttemptResponse.model_validate(row)

    def update(self, item_id: int, data: AttemptUpdate) -> Optional[AttemptResponse]:
        row = self._session.get(AttemptORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AttemptResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AttemptORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
