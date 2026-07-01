from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user_profile.user_profile_dto import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from src.orm.user_profile.user_profile_orm import UserProfileORM


class SQLAlchemyUserProfileRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UserProfileResponse]:
        row = self._session.get(UserProfileORM, item_id)
        return UserProfileResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserProfileResponse]:
        rows = self._session.query(UserProfileORM).offset(skip).limit(limit).all()
        return [UserProfileResponse.model_validate(r) for r in rows]

    def create(self, data: UserProfileCreate) -> UserProfileResponse:
        row = UserProfileORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserProfileResponse.model_validate(row)

    def update(self, item_id: int, data: UserProfileUpdate) -> Optional[UserProfileResponse]:
        row = self._session.get(UserProfileORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UserProfileResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(UserProfileORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
