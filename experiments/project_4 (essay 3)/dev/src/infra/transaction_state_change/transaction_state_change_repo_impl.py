from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.transaction_state_change.transaction_state_change_dto import TransactionStateChangeCreate, TransactionStateChangeUpdate, TransactionStateChangeResponse
from src.orm.transaction_state_change.transaction_state_change_orm import TransactionStateChangeORM


class SQLAlchemyTransactionStateChangeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TransactionStateChangeResponse]:
        row = self._session.get(TransactionStateChangeORM, item_id)
        return TransactionStateChangeResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransactionStateChangeResponse]:
        rows = self._session.query(TransactionStateChangeORM).offset(skip).limit(limit).all()
        return [TransactionStateChangeResponse.model_validate(r) for r in rows]

    def create(self, data: TransactionStateChangeCreate) -> TransactionStateChangeResponse:
        row = TransactionStateChangeORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TransactionStateChangeResponse.model_validate(row)

    def update(self, item_id: int, data: TransactionStateChangeUpdate) -> Optional[TransactionStateChangeResponse]:
        row = self._session.get(TransactionStateChangeORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TransactionStateChangeResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TransactionStateChangeORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
