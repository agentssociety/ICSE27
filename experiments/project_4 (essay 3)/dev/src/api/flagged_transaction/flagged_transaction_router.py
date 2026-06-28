from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.flagged_transaction.flagged_transaction_dto import (
    FlaggedTransactionResponse,
    FlaggedTransactionListResponse,
    FlagReviewRequest,
)
from src.service.flagged_transaction.flagged_transaction_service import FlaggedTransactionService

router = APIRouter()


def _service(db: Session = Depends(get_db)) -> FlaggedTransactionService:
    return FlaggedTransactionService(db)


@router.get("", response_model=FlaggedTransactionListResponse)
def list_flagged_transactions(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    service: FlaggedTransactionService = Depends(_service),
):
    return service.get_flagged_transactions(
        status_filter=status,
        limit=limit,
        offset=offset,
    )


@router.get("/{item_id}", response_model=FlaggedTransactionResponse)
def get_flagged_transaction(
    item_id: str,
    service: FlaggedTransactionService = Depends(_service),
):
    item = service.get_flagged_transaction_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FlaggedTransaction not found",
        )
    return item


@router.post("/{item_id}/review", response_model=FlaggedTransactionResponse)
def review_flagged_transaction(
    item_id: str,
    body: FlagReviewRequest,
    service: FlaggedTransactionService = Depends(_service),
):
    item = service.review_flagged_transaction(
        transaction_id=item_id,
        reviewer_id=body.reviewer_id,
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FlaggedTransaction not found",
        )
    return item

