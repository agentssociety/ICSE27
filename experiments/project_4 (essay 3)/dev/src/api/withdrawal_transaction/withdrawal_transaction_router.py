from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalCreateRequest, WithdrawalResponse
from src.infra.withdrawal_transaction.withdrawal_transaction_repo_impl import SQLAlchemyWithdrawalTransactionRepository
from src.service.withdrawal_transaction.withdrawal_transaction_service import WithdrawalTransactionServiceImpl
from decimal import Decimal

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalTransactionRepository:
    return SQLAlchemyWithdrawalTransactionRepository(db)

def _service(db: Session = Depends(get_db)) -> WithdrawalTransactionServiceImpl:
    return WithdrawalTransactionServiceImpl(db)

@router.get("", response_model=list[WithdrawalResponse])
def list_withdrawal_transactions(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repo: SQLAlchemyWithdrawalTransactionRepository = Depends(_repo)
):
    items = repo.get_all(skip=skip, limit=limit)
    if status:
        items = [i for i in items if i.status == status]
    return items

@router.get("/{item_id}", response_model=WithdrawalResponse)
def get_withdrawal_transaction(
    item_id: str,
    repo: SQLAlchemyWithdrawalTransactionRepository = Depends(_repo)
):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WithdrawalTransaction not found"
        )
    return item

@router.post("", response_model=WithdrawalResponse, status_code=status.HTTP_201_CREATED)
def create_withdrawal_transaction(
    data: WithdrawalCreateRequest,
    service: WithdrawalTransactionServiceImpl = Depends(_service)
):
    try:
        return service.create_withdrawal(
            account_id=data.account_id,
            amount=data.amount
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{item_id}/fail", response_model=WithdrawalResponse)
def fail_withdrawal_transaction(
    item_id: str,
    repo: SQLAlchemyWithdrawalTransactionRepository = Depends(_repo)
):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WithdrawalTransaction not found"
        )
    # Update status to failed - in real implementation, this would update DB
    from sqlalchemy import update
    from src.orm.withdrawal_transaction.withdrawal_transaction_orm import WithdrawalTransactionORM
    db = next(get_db())
    db.execute(update(WithdrawalTransactionORM).where(
        WithdrawalTransactionORM.id == item_id
    ).values(status="failed"))
    db.commit()
    return repo.get_by_id(item_id)
