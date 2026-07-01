from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.friend_request.friend_request_dto import FriendRequestCreate, FriendRequestUpdate, FriendRequestResponse
from src.orm.friend_request.friend_request_orm import FriendRequestORM


class SQLAlchemyFriendRequestRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[FriendRequestResponse]:
        row = self._session.get(FriendRequestORM, item_id)
        return FriendRequestResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FriendRequestResponse]:
        rows = self._session.query(FriendRequestORM).offset(skip).limit(limit).all()
        return [FriendRequestResponse.model_validate(r) for r in rows]

    def create(self, data: FriendRequestCreate) -> FriendRequestResponse:
        row = FriendRequestORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return FriendRequestResponse.model_validate(row)

    def update(self, item_id: int, data: FriendRequestUpdate) -> Optional[FriendRequestResponse]:
        row = self._session.get(FriendRequestORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return FriendRequestResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(FriendRequestORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
