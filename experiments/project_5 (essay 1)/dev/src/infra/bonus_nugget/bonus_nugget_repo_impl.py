from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.bonus_nugget.bonus_nugget_dto import BonusNuggetCreate, BonusNuggetUpdate, BonusNuggetResponse
from src.orm.bonus_nugget.bonus_nugget_orm import BonusNuggetORM


class SQLAlchemyBonusNuggetRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BonusNuggetResponse]:
        row = self._session.get(BonusNuggetORM, item_id)
        return BonusNuggetResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BonusNuggetResponse]:
        rows = self._session.query(BonusNuggetORM).offset(skip).limit(limit).all()
        return [BonusNuggetResponse.model_validate(r) for r in rows]

    def create(self, data: BonusNuggetCreate) -> BonusNuggetResponse:
        row = BonusNuggetORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BonusNuggetResponse.model_validate(row)

    def update(self, item_id: int, data: BonusNuggetUpdate) -> Optional[BonusNuggetResponse]:
        row = self._session.get(BonusNuggetORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BonusNuggetResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BonusNuggetORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
