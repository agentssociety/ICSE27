from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.question.question_dto import QuestionCreate, QuestionUpdate, QuestionResponse
from src.orm.question.question_orm import QuestionORM


class SQLAlchemyQuestionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[QuestionResponse]:
        row = self._session.get(QuestionORM, item_id)
        return QuestionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[QuestionResponse]:
        rows = self._session.query(QuestionORM).offset(skip).limit(limit).all()
        return [QuestionResponse.model_validate(r) for r in rows]

    def create(self, data: QuestionCreate) -> QuestionResponse:
        row = QuestionORM(**data.model_dump(exclude_unset=True, mode='json'))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return QuestionResponse.model_validate(row)

    def update(self, item_id: int, data: QuestionUpdate) -> Optional[QuestionResponse]:
        row = self._session.get(QuestionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True, mode='json').items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return QuestionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(QuestionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
