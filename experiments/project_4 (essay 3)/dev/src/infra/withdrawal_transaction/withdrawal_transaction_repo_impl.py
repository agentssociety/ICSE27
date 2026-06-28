from __future__ import annotations

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalCreateRequest, WithdrawalResponse
from src.orm.withdrawal_transaction.withdrawal_transaction_orm import WithdrawalTransactionORM


class SQLAlchemyWithdrawalTransactionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[WithdrawalResponse]:
        row = self._session.get(WithdrawalTransactionORM, item_id)
        if row is None:
            return None
        return WithdrawalResponse(
            id=row.id,
            account_id=row.account_id,
            amount=row.amount,
            status=row.status,
            timestamp=row.timestamp
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[WithdrawalResponse]:
        rows = self._session.query(WithdrawalTransactionORM).offset(skip).limit(limit).all()
        return [
            WithdrawalResponse(
                id=row.id,
                account_id=row.account_id,
                amount=row.amount,
                status=row.status,
                timestamp=row.timestamp
            )
            for row in rows
        ]

    def create(self, data: WithdrawalCreateRequest) -> WithdrawalResponse:
        from src.domain.withdrawal_transaction.WithdrawalTransaction import WithdrawalTransaction, WithdrawalStatus
        import uuid
        from datetime import datetime

        transaction = WithdrawalTransaction.create(
            account_id=data.account_id,
            amount=data.amount
        )
        row = WithdrawalTransactionORM(
            id=transaction.id,
            account_id=transaction.account_id,
            amount=float(transaction.amount),
            status=transaction.status.value,
            timestamp=transaction.timestamp
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return WithdrawalResponse(
            id=row.id,
            account_id=row.account_id,
            amount=row.amount,
            status=row.status,
            timestamp=row.timestamp
        )

    def delete(self, item_id: str) -> bool:
        row = self._session.get(WithdrawalTransactionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
