from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.comment.comment_dto import CommentCreate, CommentUpdate, CommentResponse
from src.orm.comment.comment_orm import CommentORM


class SQLAlchemyCommentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[CommentResponse]:
        row = self._session.get(CommentORM, item_id)
        return CommentResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CommentResponse]:
        rows = self._session.query(CommentORM).offset(skip).limit(limit).all()
        return [CommentResponse.model_validate(r) for r in rows]

    def create(self, data: CommentCreate) -> CommentResponse:
        row = CommentORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CommentResponse.model_validate(row)

    def update(self, item_id: int, data: CommentUpdate) -> Optional[CommentResponse]:
        row = self._session.get(CommentORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CommentResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(CommentORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
