from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.withdrawal_request.withdrawal_request_dto import WithdrawalRequestCreate, WithdrawalRequestUpdate, WithdrawalRequestResponse
from src.orm.withdrawal_request.withdrawal_request_orm import WithdrawalRequestORM


class SQLAlchemyWithdrawalRequestRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[WithdrawalRequestResponse]:
        row = self._session.get(WithdrawalRequestORM, item_id)
        return WithdrawalRequestResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[WithdrawalRequestResponse]:
        rows = self._session.query(WithdrawalRequestORM).offset(skip).limit(limit).all()
        return [WithdrawalRequestResponse.model_validate(r) for r in rows]

    def create(self, data: WithdrawalRequestCreate) -> WithdrawalRequestResponse:
        row = WithdrawalRequestORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalRequestResponse.model_validate(row)

    def update(self, item_id: int, data: WithdrawalRequestUpdate) -> Optional[WithdrawalRequestResponse]:
        row = self._session.get(WithdrawalRequestORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalRequestResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(WithdrawalRequestORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
