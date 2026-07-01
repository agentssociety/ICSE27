from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.friendship.friendship_dto import FriendshipCreate, FriendshipUpdate, FriendshipResponse
from src.orm.friendship.friendship_orm import FriendshipORM


class SQLAlchemyFriendshipRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[FriendshipResponse]:
        row = self._session.get(FriendshipORM, item_id)
        return FriendshipResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FriendshipResponse]:
        rows = self._session.query(FriendshipORM).offset(skip).limit(limit).all()
        return [FriendshipResponse.model_validate(r) for r in rows]

    def create(self, data: FriendshipCreate) -> FriendshipResponse:
        row = FriendshipORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return FriendshipResponse.model_validate(row)

    def update(self, item_id: int, data: FriendshipUpdate) -> Optional[FriendshipResponse]:
        row = self._session.get(FriendshipORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return FriendshipResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(FriendshipORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
