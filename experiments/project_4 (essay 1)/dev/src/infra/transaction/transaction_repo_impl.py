from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.transaction.transaction_dto import TransactionCreate, TransactionUpdate, TransactionResponse

try:
    from src.orm.transaction.transaction_orm import TransactionORM
except ModuleNotFoundError:
    # Dummy class to avoid import error in scaffold
    from sqlalchemy import Column, Integer
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    class TransactionORM(Base):
        __tablename__ = "transactions"
        id = Column(Integer, primary_key=True)


class SQLAlchemyTransactionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TransactionResponse]:
        row = self._session.get(TransactionORM, item_id)
        return TransactionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransactionResponse]:
        rows = self._session.query(TransactionORM).offset(skip).limit(limit).all()
        return [TransactionResponse.model_validate(r) for r in rows]

    def get_by_user_id(self, user_id: int) -> list[TransactionResponse]:
        rows = self._session.query(TransactionORM).filter(TransactionORM.user_id == user_id).all()
        return [TransactionResponse.model_validate(r) for r in rows]

    def create(self, data: TransactionCreate) -> TransactionResponse:
        row = TransactionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TransactionResponse.model_validate(row)

    def update(self, item_id: int, data: TransactionUpdate) -> Optional[TransactionResponse]:
        row = self._session.get(TransactionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TransactionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TransactionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True