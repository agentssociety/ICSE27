from __future__ import annotations

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionResponse, FlaggedTransactionListResponse
from src.orm.flagged_transaction.flagged_transaction_orm import FlaggedTransactionORM


class SQLAlchemyFlaggedTransactionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[FlaggedTransactionResponse]:
        row = self._session.get(FlaggedTransactionORM, item_id)
        if row is None:
            return None
        return FlaggedTransactionResponse(
            id=row.id,
            withdrawal_id=row.withdrawal_id,
            reason=row.reason,
            flagged_at=row.flagged_at,
            reviewed_by=row.reviewed_by,
            status=row.status,
        )

    def get_all(
        self,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[FlaggedTransactionResponse]:
        query = self._session.query(FlaggedTransactionORM)
        if status_filter:
            query = query.filter(FlaggedTransactionORM.status == status_filter)
        rows = query.order_by(FlaggedTransactionORM.flagged_at.desc()).offset(skip).limit(limit).all()
        return [
            FlaggedTransactionResponse(
                id=row.id,
                withdrawal_id=row.withdrawal_id,
                reason=row.reason,
                flagged_at=row.flagged_at,
                reviewed_by=row.reviewed_by,
                status=row.status,
            )
            for row in rows
        ]

    def count(self, status_filter: Optional[str] = None) -> int:
        query = self._session.query(FlaggedTransactionORM)
        if status_filter:
            query = query.filter(FlaggedTransactionORM.status == status_filter)
        return query.count()

    def create(self, data: FlaggedTransactionResponse) -> FlaggedTransactionResponse:
        row = FlaggedTransactionORM(
            id=data.id,
            withdrawal_id=data.withdrawal_id,
            reason=data.reason,
            flagged_at=data.flagged_at,
            reviewed_by=data.reviewed_by,
            status=data.status,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return FlaggedTransactionResponse(
            id=row.id,
            withdrawal_id=row.withdrawal_id,
            reason=row.reason,
            flagged_at=row.flagged_at,
            reviewed_by=row.reviewed_by,
            status=row.status,
        )

    def update_review(
        self, item_id: str, reviewer_id: str
    ) -> Optional[FlaggedTransactionResponse]:
        row = self._session.get(FlaggedTransactionORM, item_id)
        if row is None:
            return None
        row.reviewed_by = reviewer_id
        row.status = "reviewed"
        self._session.commit()
        self._session.refresh(row)
        return FlaggedTransactionResponse(
            id=row.id,
            withdrawal_id=row.withdrawal_id,
            reason=row.reason,
            flagged_at=row.flagged_at,
            reviewed_by=row.reviewed_by,
            status=row.status,
        )

