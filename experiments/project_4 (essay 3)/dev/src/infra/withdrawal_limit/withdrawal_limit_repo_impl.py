from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.withdrawal_limit.withdrawal_limit_dto import WithdrawalLimitCreate, WithdrawalLimitUpdate, WithdrawalLimitResponse
from src.orm.withdrawal_limit.withdrawal_limit_orm import WithdrawalLimitORM


class SQLAlchemyWithdrawalLimitRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[WithdrawalLimitResponse]:
        row = self._session.get(WithdrawalLimitORM, item_id)
        return WithdrawalLimitResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[WithdrawalLimitResponse]:
        rows = self._session.query(WithdrawalLimitORM).offset(skip).limit(limit).all()
        return [WithdrawalLimitResponse.model_validate(r) for r in rows]

    def create(self, data: WithdrawalLimitCreate) -> WithdrawalLimitResponse:
        row = WithdrawalLimitORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalLimitResponse.model_validate(row)

    def update(self, item_id: int, data: WithdrawalLimitUpdate) -> Optional[WithdrawalLimitResponse]:
        row = self._session.get(WithdrawalLimitORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalLimitResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(WithdrawalLimitORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
