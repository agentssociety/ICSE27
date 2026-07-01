from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.bookmark.bookmark_dto import BookmarkCreate, BookmarkUpdate, BookmarkResponse
from src.orm.bookmark.bookmark_orm import BookmarkORM


class SQLAlchemyBookmarkRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BookmarkResponse]:
        row = self._session.get(BookmarkORM, item_id)
        return BookmarkResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BookmarkResponse]:
        rows = self._session.query(BookmarkORM).offset(skip).limit(limit).all()
        return [BookmarkResponse.model_validate(r) for r in rows]

    def create(self, data: BookmarkCreate) -> BookmarkResponse:
        row = BookmarkORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BookmarkResponse.model_validate(row)

    def update(self, item_id: int, data: BookmarkUpdate) -> Optional[BookmarkResponse]:
        row = self._session.get(BookmarkORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BookmarkResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BookmarkORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
