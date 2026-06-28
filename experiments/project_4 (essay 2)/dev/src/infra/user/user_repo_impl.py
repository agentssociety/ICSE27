from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse
from src.orm.user.user_orm import UserORM

"""
Infra layer for the User domain class

Package: infra.user
Layer: infra
Related tasks: #88, #89, #93, #94, #95
Requirement coverage:
- Card and PIN Authentication Requirement
- Account Lock After Three Consecutive Failed PIN Attempts
- Admin Interface for Flagged Transactions Review
- Manual Lock/Unlock User Accounts
- Audit Log Maintenance
"""


class SQLAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        return UserResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        rows = self._session.query(UserORM).offset(skip).limit(limit).all()
        return [UserResponse.model_validate(r) for r in rows]

    def create(self, data: UserCreateRequest) -> UserResponse:
        row = UserORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserResponse.model_validate(row)

    def update(self, item_id: str, data: UserUpdateRequest) -> Optional[UserResponse]:
        row = self._session.get(UserORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
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
