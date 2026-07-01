from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.verified_badge.verified_badge_dto import VerifiedBadgeCreate, VerifiedBadgeUpdate, VerifiedBadgeResponse
from src.orm.verified_badge.verified_badge_orm import VerifiedBadgeORM


class SQLAlchemyVerifiedBadgeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[VerifiedBadgeResponse]:
        row = self._session.get(VerifiedBadgeORM, item_id)
        return VerifiedBadgeResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[VerifiedBadgeResponse]:
        rows = self._session.query(VerifiedBadgeORM).offset(skip).limit(limit).all()
        return [VerifiedBadgeResponse.model_validate(r) for r in rows]

    def create(self, data: VerifiedBadgeCreate) -> VerifiedBadgeResponse:
        row = VerifiedBadgeORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return VerifiedBadgeResponse.model_validate(row)

    def update(self, item_id: int, data: VerifiedBadgeUpdate) -> Optional[VerifiedBadgeResponse]:
        row = self._session.get(VerifiedBadgeORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return VerifiedBadgeResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(VerifiedBadgeORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
