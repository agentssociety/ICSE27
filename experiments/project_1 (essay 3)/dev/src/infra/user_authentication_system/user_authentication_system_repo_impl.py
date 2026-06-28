from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user_authentication_system.user_authentication_system_dto import UserAuthenticationSystemCreate, UserAuthenticationSystemUpdate, UserAuthenticationSystemResponse
from src.orm.user_authentication_system.user_authentication_system_orm import UserAuthenticationSystemORM


class SQLAlchemyUserAuthenticationSystemRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UserAuthenticationSystemResponse]:
        row = self._session.get(UserAuthenticationSystemORM, item_id)
        return UserAuthenticationSystemResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserAuthenticationSystemResponse]:
        rows = self._session.query(UserAuthenticationSystemORM).offset(skip).limit(limit).all()
        return [UserAuthenticationSystemResponse.model_validate(r) for r in rows]

    def create(self, data: UserAuthenticationSystemCreate) -> UserAuthenticationSystemResponse:
        row = UserAuthenticationSystemORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserAuthenticationSystemResponse.model_validate(row)

    def update(self, item_id: int, data: UserAuthenticationSystemUpdate) -> Optional[UserAuthenticationSystemResponse]:
        row = self._session.get(UserAuthenticationSystemORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UserAuthenticationSystemResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(UserAuthenticationSystemORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
