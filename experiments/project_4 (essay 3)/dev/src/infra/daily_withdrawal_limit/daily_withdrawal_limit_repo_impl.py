from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.daily_withdrawal_limit.daily_withdrawal_limit_dto import DailyWithdrawalLimitCreateRequest, DailyWithdrawalLimitUpdateRequest, DailyWithdrawalLimitResponse
from src.orm.daily_withdrawal_limit.daily_withdrawal_limit_orm import DailyWithdrawalLimitORM


class SQLAlchemyDailyWithdrawalLimitRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[DailyWithdrawalLimitResponse]:
        row = self._session.get(DailyWithdrawalLimitORM, item_id)
        return DailyWithdrawalLimitResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[DailyWithdrawalLimitResponse]:
        rows = self._session.query(DailyWithdrawalLimitORM).offset(skip).limit(limit).all()
        return [DailyWithdrawalLimitResponse.model_validate(r) for r in rows]

    def create(self, data: DailyWithdrawalLimitCreateRequest) -> DailyWithdrawalLimitResponse:
        row = DailyWithdrawalLimitORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return DailyWithdrawalLimitResponse.model_validate(row)

    def update(self, item_id: int, data: DailyWithdrawalLimitUpdateRequest) -> Optional[DailyWithdrawalLimitResponse]:
        row = self._session.get(DailyWithdrawalLimitORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return DailyWithdrawalLimitResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(DailyWithdrawalLimitORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
