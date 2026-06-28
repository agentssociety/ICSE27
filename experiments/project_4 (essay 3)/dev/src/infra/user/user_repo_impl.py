from __future__ import annotations

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse, UserListResponse
from src.orm.user.user_orm import UserORM


class SQLAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        return UserResponse.model_validate(row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        rows = self._session.query(UserORM).order_by(UserORM.created_at.desc()).offset(skip).limit(limit).all()
        return [UserResponse.model_validate(r) for r in rows]

    def create(self, data: UserCreateRequest) -> UserResponse:
        from src.domain.user.User import User, UserRole, UserStatus
        import uuid
        now = datetime.utcnow()
        role = UserRole.REGULAR_USER if data.role == "regular_user" else UserRole.ADMIN
        user = User.create(
            username=data.username,
            email=data.email,
            password_hash=data.password_hash,
            role=role,
        )
        row = UserORM(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role.value,
            status=user.status.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def update(self, item_id: str, data: UserUpdateRequest) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            if hasattr(row, key):
                setattr(row, key, value)
        row.updated_at = datetime.utcnow()
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def deactivate(self, item_id: str) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        row.status = "inactive"
        row.updated_at = datetime.utcnow()
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def activate(self, item_id: str) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        row.status = "active"
        row.updated_at = datetime.utcnow()
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def delete(self, item_id: str) -> bool:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True

    def count(self) -> int:
        return self._session.query(UserORM).count()
