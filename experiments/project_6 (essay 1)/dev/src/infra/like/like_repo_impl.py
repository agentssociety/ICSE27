from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.like.like_dto import LikeCreate, LikeUpdate, LikeResponse
from src.orm.like.like_orm import LikeORM


class SQLAlchemyLikeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[LikeResponse]:
        row = self._session.get(LikeORM, item_id)
        return LikeResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[LikeResponse]:
        rows = self._session.query(LikeORM).offset(skip).limit(limit).all()
        return [LikeResponse.model_validate(r) for r in rows]

    def create(self, data: LikeCreate) -> LikeResponse:
        row = LikeORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return LikeResponse.model_validate(row)

    def update(self, item_id: int, data: LikeUpdate) -> Optional[LikeResponse]:
        row = self._session.get(LikeORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return LikeResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(LikeORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
