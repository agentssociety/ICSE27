from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.profile.profile_dto import ProfileCreate, ProfileUpdate, ProfileResponse
from src.orm.profile.profile_orm import ProfileORM


class SQLAlchemyProfileRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ProfileResponse]:
        row = self._session.get(ProfileORM, item_id)
        return ProfileResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProfileResponse]:
        rows = self._session.query(ProfileORM).offset(skip).limit(limit).all()
        return [ProfileResponse.model_validate(r) for r in rows]

    def create(self, data: ProfileCreate) -> ProfileResponse:
        row = ProfileORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ProfileResponse.model_validate(row)

    def update(self, item_id: int, data: ProfileUpdate) -> Optional[ProfileResponse]:
        row = self._session.get(ProfileORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ProfileResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ProfileORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
