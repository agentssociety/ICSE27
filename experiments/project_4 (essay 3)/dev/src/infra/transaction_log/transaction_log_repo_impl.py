from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.transaction_log.transaction_log_dto import TransactionLogCreate, TransactionLogUpdate, TransactionLogResponse
from src.orm.transaction_log.transaction_log_orm import TransactionLogORM


class SQLAlchemyTransactionLogRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TransactionLogResponse]:
        row = self._session.get(TransactionLogORM, item_id)
        return TransactionLogResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransactionLogResponse]:
        rows = self._session.query(TransactionLogORM).offset(skip).limit(limit).all()
        return [TransactionLogResponse.model_validate(r) for r in rows]

    def create(self, data: TransactionLogCreate) -> TransactionLogResponse:
        row = TransactionLogORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TransactionLogResponse.model_validate(row)

    def update(self, item_id: int, data: TransactionLogUpdate) -> Optional[TransactionLogResponse]:
        row = self._session.get(TransactionLogORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TransactionLogResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TransactionLogORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
