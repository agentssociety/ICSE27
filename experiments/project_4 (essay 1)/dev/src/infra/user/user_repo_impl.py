from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user.user_dto import UserCreate, UserUpdate, UserResponse


class SQLAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UserResponse]:
        from src.orm.user.user_orm import UserORM

        row = self._session.get(UserORM, item_id)
        return UserResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        from src.orm.user.user_orm import UserORM

        rows = self._session.query(UserORM).offset(skip).limit(limit).all()
        return [UserResponse.model_validate(r) for r in rows]

    def create(self, data: UserCreate) -> UserResponse:
        from src.orm.user.user_orm import UserORM

        row = UserORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def update(self, item_id: int, data: UserUpdate) -> Optional[UserResponse]:
        from src.orm.user.user_orm import UserORM

        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        from src.orm.user.user_orm import UserORM

        row = self._session.get(UserORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
