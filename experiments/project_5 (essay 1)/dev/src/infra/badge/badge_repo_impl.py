from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.badge.badge_dto import BadgeCreate, BadgeUpdate, BadgeResponse
from src.orm.badge.badge_orm import BadgeORM


class SQLAlchemyBadgeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BadgeResponse]:
        row = self._session.get(BadgeORM, item_id)
        return BadgeResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BadgeResponse]:
        rows = self._session.query(BadgeORM).offset(skip).limit(limit).all()
        return [BadgeResponse.model_validate(r) for r in rows]

    def create(self, data: BadgeCreate) -> BadgeResponse:
        row = BadgeORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BadgeResponse.model_validate(row)

    def update(self, item_id: int, data: BadgeUpdate) -> Optional[BadgeResponse]:
        row = self._session.get(BadgeORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BadgeResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BadgeORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
