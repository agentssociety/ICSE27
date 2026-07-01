from __future__ import annotations

from typing import Optional, Any

from sqlalchemy.orm import Session

try:
    from src.dto.exam_session.exam_session_dto import ExamSessionCreate, ExamSessionUpdate, ExamSessionResponse
except ImportError:
    ExamSessionCreate = Any
    ExamSessionUpdate = Any
    ExamSessionResponse = Any

from src.orm.exam_session.exam_session_orm import ExamSessionORM


class SQLAlchemyExamSessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ExamSessionResponse]:
        row = self._session.get(ExamSessionORM, item_id)
        return ExamSessionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ExamSessionResponse]:
        rows = self._session.query(ExamSessionORM).offset(skip).limit(limit).all()
        return [ExamSessionResponse.model_validate(r) for r in rows]

    def create(self, data: ExamSessionCreate) -> ExamSessionResponse:
        row = ExamSessionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ExamSessionResponse.model_validate(row)

    def update(self, item_id: int, data: ExamSessionUpdate) -> Optional[ExamSessionResponse]:
        row = self._session.get(ExamSessionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ExamSessionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ExamSessionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True