from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user_database.user_database_dto import User_DatabaseCreate, User_DatabaseUpdate, User_DatabaseResponse
from src.orm.user_database.user_database_orm import User_DatabaseORM


class SQLAlchemyUser_DatabaseRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[User_DatabaseResponse]:
        row = self._session.get(User_DatabaseORM, item_id)
        return User_DatabaseResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User_DatabaseResponse]:
        rows = self._session.query(User_DatabaseORM).offset(skip).limit(limit).all()
        return [User_DatabaseResponse.model_validate(r) for r in rows]

    def create(self, data: User_DatabaseCreate) -> User_DatabaseResponse:
        row = User_DatabaseORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return User_DatabaseResponse.model_validate(row)

    def update(self, item_id: int, data: User_DatabaseUpdate) -> Optional[User_DatabaseResponse]:
        row = self._session.get(User_DatabaseORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return User_DatabaseResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(User_DatabaseORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
