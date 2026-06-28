from __future__ import annotations

from typing import Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionResponse, FlaggedTransactionListResponse
from src.infra.flagged_transaction.flagged_transaction_repo_impl import SQLAlchemyFlaggedTransactionRepository
from src.domain.flagged_transaction.FlaggedTransaction import FlaggedTransaction, FlagStatus, DetectionEngine


class FlaggedTransactionService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = SQLAlchemyFlaggedTransactionRepository(session)
        self._detection_engine = DetectionEngine()

    def flag_withdrawal(
        self,
        withdrawal_id: str,
        account_id: str,
        amount: float,
        timestamp: datetime,
        all_withdrawals: list[dict],
    ) -> FlaggedTransactionResponse | None:
        reasons = self._detection_engine.evaluate(
            withdrawal_id=withdrawal_id,
            account_id=account_id,
            amount=amount,
            timestamp=timestamp,
            all_withdrawals=all_withdrawals,
        )
        if not reasons:
            return None

        reason_str = "; ".join(sorted(reasons))
        flagged = FlaggedTransaction.create(
            withdrawal_id=withdrawal_id,
            reason=reason_str,
        )
        dto = FlaggedTransactionResponse(
            id=flagged.id,
            withdrawal_id=flagged.withdrawal_id,
            reason=flagged.reason,
            flagged_at=flagged.flagged_at,
            reviewed_by=flagged.reviewed_by,
            status=flagged.status.value,
        )
        return self._repo.create(dto)

    def get_flagged_transactions(
        self,
        status_filter: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> FlaggedTransactionListResponse:
        items = self._repo.get_all(
            status_filter=status_filter,
            skip=offset,
            limit=limit,
        )
        total = self._repo.count(status_filter=status_filter)
        return FlaggedTransactionListResponse(items=items, total=total)

    def get_flagged_transaction_by_id(
        self, transaction_id: str
    ) -> Optional[FlaggedTransactionResponse]:
        return self._repo.get_by_id(transaction_id)

    def review_flagged_transaction(
        self, transaction_id: str, reviewer_id: str
    ) -> Optional[FlaggedTransactionResponse]:
        return self._repo.update_review(transaction_id, reviewer_id)

