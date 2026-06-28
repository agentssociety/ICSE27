from __future__ import annotations

try:
    from src.orm.withdrawal_record.withdrawal_record_orm import WithdrawalRecordORM
except Exception:
    WithdrawalRecordORM = None

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.withdrawal_record.withdrawal_record_dto import WithdrawalRecordCreate, WithdrawalRecordUpdate, WithdrawalRecordResponse


class SQLAlchemyWithdrawalRecordRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[WithdrawalRecordResponse]:
        row = self._session.get(WithdrawalRecordORM, item_id)
        return WithdrawalRecordResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[WithdrawalRecordResponse]:
        rows = self._session.query(WithdrawalRecordORM).offset(skip).limit(limit).all()
        return [WithdrawalRecordResponse.model_validate(r) for r in rows]

    def create(self, data: WithdrawalRecordCreate) -> WithdrawalRecordResponse:
        row = WithdrawalRecordORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalRecordResponse.model_validate(row)

    def update(self, item_id: int, data: WithdrawalRecordUpdate) -> Optional[WithdrawalRecordResponse]:
        row = self._session.get(WithdrawalRecordORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalRecordResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(WithdrawalRecordORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True