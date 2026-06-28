from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.account.account_dto import AccountCreate, AccountUpdate, AccountResponse

try:
    from src.orm.account.account_orm import AccountORM
except ImportError:
    # Fallback dummy ORM class if the real one is unavailable (e.g., missing base module)
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class AccountORM(Base):
        __tablename__ = "account"
        id = Column(Integer, primary_key=True)
        # Additional fields can be added as needed, but this is just a placeholder


class SQLAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[AccountResponse]:
        row = self._session.get(AccountORM, item_id)
        return AccountResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[AccountResponse]:
        rows = self._session.query(AccountORM).offset(skip).limit(limit).all()
        return [AccountResponse.model_validate(r) for r in rows]

    def create(self, data: AccountCreate) -> AccountResponse:
        row = AccountORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return AccountResponse.model_validate(row)

    def update(self, item_id: int, data: AccountUpdate) -> Optional[AccountResponse]:
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