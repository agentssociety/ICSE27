from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.account.account_dto import AccountCreateRequest, AccountUpdateRequest, AccountResponse
from src.orm.account.account_orm import AccountORM


class SQLAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AccountResponse]:
        row = self._session.get(AccountORM, item_id)
        return AccountResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AccountResponse]:
        rows = self._session.query(AccountORM).offset(skip).limit(limit).all()
        return [AccountResponse.model_validate(r) for r in rows]

    def create(self, data: AccountCreateRequest) -> AccountResponse:
        row = AccountORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AccountResponse.model_validate(row)

    def update(self, item_id: int, data: AccountUpdateRequest) -> Optional[AccountResponse]:
        row = self._session.get(AccountORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AccountResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(AccountORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
