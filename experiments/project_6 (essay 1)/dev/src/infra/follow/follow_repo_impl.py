from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.follow.follow_dto import FollowCreateDTO as FollowCreate, FollowUpdateDTO as FollowUpdate, FollowResponseDTO as FollowResponse
from src.orm.follow.follow_orm import FollowORM


class SQLAlchemyFollowRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[FollowResponse]:
        row = self._session.get(FollowORM, item_id)
        return FollowResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FollowResponse]:
        rows = self._session.query(FollowORM).offset(skip).limit(limit).all()
        return [FollowResponse.model_validate(r) for r in rows]

    def create(self, data: FollowCreate) -> FollowResponse:
        row = FollowORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return FollowResponse.model_validate(row)

    def update(self, item_id: int, data: FollowUpdate) -> Optional[FollowResponse]:
        row = self._session.get(FollowORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return FollowResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(FollowORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True