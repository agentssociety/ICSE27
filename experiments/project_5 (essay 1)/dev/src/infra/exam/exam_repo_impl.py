from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.exam.exam_dto import ExamCreate, ExamUpdate, ExamResponse
from src.orm.exam.exam_orm import ExamORM


class SQLAlchemyExamRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ExamResponse]:
        row = self._session.get(ExamORM, item_id)
        return ExamResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ExamResponse]:
        rows = self._session.query(ExamORM).offset(skip).limit(limit).all()
        return [ExamResponse.model_validate(r) for r in rows]

    def create(self, data: ExamCreate) -> ExamResponse:
        row = ExamORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ExamResponse.model_validate(row)

    def update(self, item_id: int, data: ExamUpdate) -> Optional[ExamResponse]:
        row = self._session.get(ExamORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ExamResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ExamORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
