from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.user_account.user_account_dto import UserAccountCreate, UserAccountUpdate, UserAccountResponse
from src.orm.user_account.user_account_orm import UserAccountORM


class SQLAlchemyUserAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[UserAccountResponse]:
        row = self._session.get(UserAccountORM, item_id)
        return UserAccountResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserAccountResponse]:
        rows = self._session.query(UserAccountORM).offset(skip).limit(limit).all()
        return [UserAccountResponse.model_validate(r) for r in rows]

    def create(self, data: UserAccountCreate) -> UserAccountResponse:
        row = UserAccountORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return UserAccountResponse.model_validate(row)

    def update(self, item_id: int, data: UserAccountUpdate) -> Optional[UserAccountResponse]:
        row = self._session.get(UserAccountORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return UserAccountResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(UserAccountORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
