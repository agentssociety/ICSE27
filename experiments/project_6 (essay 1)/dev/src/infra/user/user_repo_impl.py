from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user.user_dto import UserCreate, UserUpdate, UserResponse
from src.orm.user.user_orm import UserORM


class SQLAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        return UserResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        rows = self._session.query(UserORM).offset(skip).limit(limit).all()
        return [UserResponse.model_validate(r) for r in rows]

    def create(self, data: UserCreate) -> UserResponse:
        payload = data.model_dump(exclude_unset=True)
        if "password" in payload:
            payload["passwordHash"] = payload.pop("password")
        row = UserORM(**payload)
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def update(self, item_id: int, data: UserUpdate) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        payload = data.model_dump(exclude_unset=True)
        if "password" in payload:
            payload["passwordHash"] = payload.pop("password")
        for key, value in payload.items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True

    def find_by_email(self, email: str) -> Optional[UserResponse]:
        row = self._session.query(UserORM).filter(UserORM.email == email).first()
        return UserResponse.model_validate(row) if row else None

    def find_orm_by_email(self, email: str) -> Optional[UserORM]:
        return self._session.query(UserORM).filter(UserORM.email == email).first()
