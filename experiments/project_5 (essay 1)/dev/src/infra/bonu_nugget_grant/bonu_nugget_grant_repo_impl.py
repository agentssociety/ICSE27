from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.bonu_nugget_grant.bonu_nugget_grant_dto import BonuNuggetGrantCreate, BonuNuggetGrantUpdate, BonuNuggetGrantResponse
from src.orm.bonu_nugget_grant.bonu_nugget_grant_orm import BonuNuggetGrantORM


class SQLAlchemyBonuNuggetGrantRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BonuNuggetGrantResponse]:
        row = self._session.get(BonuNuggetGrantORM, item_id)
        return BonuNuggetGrantResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BonuNuggetGrantResponse]:
        rows = self._session.query(BonuNuggetGrantORM).offset(skip).limit(limit).all()
        return [BonuNuggetGrantResponse.model_validate(r) for r in rows]

    def create(self, data: BonuNuggetGrantCreate) -> BonuNuggetGrantResponse:
        row = BonuNuggetGrantORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BonuNuggetGrantResponse.model_validate(row)

    def update(self, item_id: int, data: BonuNuggetGrantUpdate) -> Optional[BonuNuggetGrantResponse]:
        row = self._session.get(BonuNuggetGrantORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BonuNuggetGrantResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BonuNuggetGrantORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
