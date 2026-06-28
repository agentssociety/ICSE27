from __future__ import annotations

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalListResponse, WithdrawalResponse
from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionListResponse, FlaggedTransactionResponse, FlagReviewRequest
from src.service.user.admin_service import AdminService

router = APIRouter()


def _admin_service(db: Session = Depends(get_db)) -> AdminService:
    return AdminService(db)


@router.get("/withdrawals", response_model=WithdrawalListResponse)
def admin_list_withdrawals(
    admin_user_id: str = Query(..., description="User ID of the admin making the request"),
    status: Optional[str] = Query(None, description="Filter by status (completed/failed/pending)"),
    date_from: Optional[datetime] = Query(None, description="Filter by date from"),
    date_to: Optional[datetime] = Query(None, description="Filter by date to"),
    amount_min: Optional[float] = Query(None, description="Minimum amount"),
    amount_max: Optional[float] = Query(None, description="Maximum amount"),
    account_id: Optional[str] = Query(None, description="Filter by account ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: AdminService = Depends(_admin_service),
):
    try:
        return service.list_all_withdrawals(
            admin_user_id=admin_user_id,
            status_filter=status,
            date_from=date_from,
            date_to=date_to,
            amount_min=amount_min,
            amount_max=amount_max,
            account_id=account_id,
            skip=skip,
            limit=limit,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/withdrawals/{withdrawal_id}", response_model=WithdrawalResponse)
def admin_get_withdrawal(
    admin_user_id: str = Query(..., description="User ID of the admin making the request"),
    withdrawal_id: str = None,
    service: AdminService = Depends(_admin_service),
):
    if not withdrawal_id:
        raise HTTPException(status_code=400, detail="withdrawal_id is required")
    try:
        item = service.get_withdrawal_detail(admin_user_id, withdrawal_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Withdrawal not found",
            )
        return item
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/flagged-transactions", response_model=FlaggedTransactionListResponse)
def admin_list_flagged_transactions(
    admin_user_id: str = Query(..., description="User ID of the admin making the request"),
    status: Optional[str] = Query(None, description="Filter by status (unreviewed/reviewed)"),
    date_from: Optional[datetime] = Query(None, description="Filter by date from"),
    date_to: Optional[datetime] = Query(None, description="Filter by date to"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: AdminService = Depends(_admin_service),
):
    try:
        return service.list_all_flagged_transactions(
            admin_user_id=admin_user_id,
            status_filter=status,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/flagged-transactions/{flagged_id}", response_model=FlaggedTransactionResponse)
def admin_get_flagged_transaction(
    admin_user_id: str = Query(..., description="User ID of the admin making the request"),
    flagged_id: str = None,
    service: AdminService = Depends(_admin_service),
):
    if not flagged_id:
        raise HTTPException(status_code=400, detail="flagged_id is required")
    try:
        item = service.get_flagged_detail(admin_user_id, flagged_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flagged transaction not found",
            )
        return item
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post("/flagged-transactions/{flagged_id}/review", response_model=FlaggedTransactionResponse)
def admin_review_flagged_transaction(
    admin_user_id: str = Query(..., description="User ID of the admin making the request"),
    flagged_id: str = None,
    service: AdminService = Depends(_admin_service),
):
    if not flagged_id:
        raise HTTPException(status_code=400, detail="flagged_id is required")
    try:
        item = service.review_flagged_transaction(admin_user_id, flagged_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flagged transaction not found",
            )
        return item
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
