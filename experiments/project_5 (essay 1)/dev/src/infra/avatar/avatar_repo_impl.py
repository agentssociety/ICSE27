from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.avatar.avatar_dto import AvatarCreate, AvatarUpdate, AvatarResponse
from src.orm.avatar.avatar_orm import AvatarORM


class SQLAlchemyAvatarRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AvatarResponse]:
        row = self._session.get(AvatarORM, item_id)
        return AvatarResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AvatarResponse]:
        rows = self._session.query(AvatarORM).offset(skip).limit(limit).all()
        return [AvatarResponse.model_validate(r) for r in rows]

    def create(self, data: AvatarCreate) -> AvatarResponse:
        row = AvatarORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AvatarResponse.model_validate(row)

    def update(self, item_id: int, data: AvatarUpdate) -> Optional[AvatarResponse]:
        row = self._session.get(AvatarORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AvatarResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AvatarORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
