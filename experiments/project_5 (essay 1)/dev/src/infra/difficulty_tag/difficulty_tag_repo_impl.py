from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.difficulty_tag.difficulty_tag_dto import DifficultyTagCreate, DifficultyTagUpdate, DifficultyTagResponse
from src.orm.difficulty_tag.difficulty_tag_orm import DifficultyTagORM


class SQLAlchemyDifficultyTagRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[DifficultyTagResponse]:
        row = self._session.get(DifficultyTagORM, item_id)
        return DifficultyTagResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[DifficultyTagResponse]:
        rows = self._session.query(DifficultyTagORM).offset(skip).limit(limit).all()
        return [DifficultyTagResponse.model_validate(r) for r in rows]

    def create(self, data: DifficultyTagCreate) -> DifficultyTagResponse:
        row = DifficultyTagORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return DifficultyTagResponse.model_validate(row)

    def update(self, item_id: int, data: DifficultyTagUpdate) -> Optional[DifficultyTagResponse]:
        row = self._session.get(DifficultyTagORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return DifficultyTagResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(DifficultyTagORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
