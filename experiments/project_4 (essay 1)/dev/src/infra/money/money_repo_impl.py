from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.money.money_dto import MoneyCreate, MoneyUpdate, MoneyResponse


class SQLAlchemyMoneyRepository:
    def __init__(self, session: Session) -> None:
        from src.orm.money.money_orm import MoneyORM  # lazy import to avoid missing base module
        self._session = session
        self._orm_class = MoneyORM

    def get_by_id(self, item_id: int) -> Optional[MoneyResponse]:
        row = self._session.get(self._orm_class, item_id)
        return MoneyResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[MoneyResponse]:
        rows = self._session.query(self._orm_class).offset(skip).limit(limit).all()
        return [MoneyResponse.model_validate(r) for r in rows]

    def create(self, data: MoneyCreate) -> MoneyResponse:
        row = self._orm_class(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return MoneyResponse.model_validate(row)

    def update(self, item_id: int, data: MoneyUpdate) -> Optional[MoneyResponse]:
        row = self._session.get(self._orm_class, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return MoneyResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(self._orm_class, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True