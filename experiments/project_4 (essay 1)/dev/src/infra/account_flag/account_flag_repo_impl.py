from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.account_flag.account_flag_dto import AccountFlagCreate, AccountFlagUpdate, AccountFlagResponse


class SQLAlchemyAccountFlagRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AccountFlagResponse]:
        from src.orm.account_flag.account_flag_orm import AccountFlagORM
        row = self._session.get(AccountFlagORM, item_id)
        return AccountFlagResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AccountFlagResponse]:
        from src.orm.account_flag.account_flag_orm import AccountFlagORM
        rows = self._session.query(AccountFlagORM).offset(skip).limit(limit).all()
        return [AccountFlagResponse.model_validate(r) for r in rows]

    def create(self, data: AccountFlagCreate) -> AccountFlagResponse:
        from src.orm.account_flag.account_flag_orm import AccountFlagORM
        row = AccountFlagORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AccountFlagResponse.model_validate(row)

    def update(self, item_id: int, data: AccountFlagUpdate) -> Optional[AccountFlagResponse]:
        from src.orm.account_flag.account_flag_orm import AccountFlagORM
        row = self._session.get(AccountFlagORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return AccountFlagResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        from src.orm.account_flag.account_flag_orm import AccountFlagORM
        row = self._session.get(AccountFlagORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True