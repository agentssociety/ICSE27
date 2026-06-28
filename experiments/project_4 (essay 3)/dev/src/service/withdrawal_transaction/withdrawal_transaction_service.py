from __future__ import annotations

from typing import Any, Optional, Protocol
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalCreateRequest, WithdrawalResponse
from src.infra.withdrawal_transaction.withdrawal_transaction_repo_impl import SQLAlchemyWithdrawalTransactionRepository
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository
from src.orm.account.account_orm import AccountORM
from src.domain.withdrawal_transaction.WithdrawalTransaction import WithdrawalTransaction, WithdrawalStatus


class WithdrawalTransactionService(Protocol):
    def create_withdrawal(self, account_id: str, amount: Decimal) -> WithdrawalResponse:
        ...
    def get_withdrawal(self, transaction_id: str) -> Optional[WithdrawalResponse]:
        ...
    def list_withdrawals(self, status: Optional[str] = None) -> list[WithdrawalResponse]:
        ...


class WithdrawalTransactionServiceImpl:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._withdrawal_repo = SQLAlchemyWithdrawalTransactionRepository(session)
        self._account_repo = SQLAlchemyAccountRepository(session)

    def create_withdrawal(self, account_id: str, amount: Decimal) -> WithdrawalResponse:
        """Atomic transaction: check balance, deduct, create record, commit or rollback."""
        from src.dto.account.account_dto import AccountResponse

        try:
            # Get account (as ORM row or DTO)
            account_row = self._session.query(AccountORM).filter(
                AccountORM.account_id == account_id
            ).first()

            if account_row is None:
                raise ValueError(f"Account {account_id} not found")

            # Check balance sufficiency
            if account_row.balance < float(amount):
                raise ValueError(f"Insufficient funds: balance {account_row.balance} < requested {float(amount)}")

            # Update balance (deduct)
            account_row.balance -= float(amount)
            self._session.flush()

            # Create withdrawal transaction
            from src.domain.withdrawal_transaction.WithdrawalTransaction import WithdrawalTransaction
            import uuid
            from datetime import datetime
            from decimal import Decimal

            transaction = WithdrawalTransaction.create(
                account_id=account_id,
                amount=Decimal(str(amount))
            )
            transaction.complete()

            # Create DB record
            from src.orm.withdrawal_transaction.withdrawal_transaction_orm import WithdrawalTransactionORM

            orm_row = WithdrawalTransactionORM(
                id=transaction.id,
                account_id=transaction.account_id,
                amount=float(amount),
                status=WithdrawalStatus.COMPLETED.value,
                timestamp=datetime.utcnow()
            )
            self._session.add(orm_row)
            self._session.flush()
            self._session.commit()

            return WithdrawalResponse(
                id=orm_row.id,
                account_id=orm_row.account_id,
                amount=Decimal(str(orm_row.amount)),
                status=orm_row.status,
                timestamp=datetime.fromisoformat(orm_row.timestamp.isoformat()) if isinstance(orm_row.timestamp, datetime) else orm_row.timestamp
            )

        except Exception as e:
            self._session.rollback()
            raise

    def get_withdrawal(self, transaction_id: str) -> Optional[WithdrawalResponse]:
        return self._withdrawal_repo.get_by_id(transaction_id)

    def list_withdrawals(self, status: Optional[str] = None) -> list[WithdrawalResponse]:
        items = self._withdrawal_repo.get_all()
        if status:
            items = [i for i in items if i.status == status]
        return items
