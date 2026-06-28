from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.account_balance.account_balance_dto import AccountBalanceCreate, AccountBalanceUpdate, AccountBalanceResponse
from src.orm.account_balance.account_balance_orm import AccountBalanceORM


class SQLAlchemyAccountBalanceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AccountBalanceResponse]:
        row = self._session.get(AccountBalanceORM, item_id)
        return AccountBalanceResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AccountBalanceResponse]:
        rows = self._session.query(AccountBalanceORM).offset(skip).limit(limit).all()
        return [AccountBalanceResponse.model_validate(r) for r in rows]

    def create(self, data: AccountBalanceCreate) -> AccountBalanceResponse:
        row = AccountBalanceORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AccountBalanceResponse.model_validate(row)

    def update(self, item_id: int, data: AccountBalanceUpdate) -> Optional[AccountBalanceResponse]:
        row = self._session.get(AccountBalanceORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AccountBalanceResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AccountBalanceORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
