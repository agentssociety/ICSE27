from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transaction.transaction_dto import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
)
from src.infra.transaction.transaction_repo_impl import SQLAlchemyTransactionRepository
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository
from src.infra.audit_log_entry.audit_log_entry_repo_impl import SQLAlchemyAuditLogEntryRepository
from src.service.transaction.transaction_service import TransactionServiceImpl

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransactionRepository:
    return SQLAlchemyTransactionRepository(db)


def _account_repo(db: Session = Depends(get_db)) -> SQLAlchemyAccountRepository:
    return SQLAlchemyAccountRepository(db)


def _audit_repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogEntryRepository:
    return SQLAlchemyAuditLogEntryRepository(db)


def _service(
    txn_repo: SQLAlchemyTransactionRepository = Depends(_repo),
    acct_repo: SQLAlchemyAccountRepository = Depends(_account_repo),
    audit_repo: SQLAlchemyAuditLogEntryRepository = Depends(_audit_repo),
) -> TransactionServiceImpl:
    return TransactionServiceImpl(
        transaction_repo=txn_repo,
        account_repo=acct_repo,
        audit_repo=audit_repo,
    )


@router.get("", response_model=list[TransactionResponse])
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    repo: SQLAlchemyTransactionRepository = Depends(_repo),
):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/flagged", response_model=list[dict])
def list_flagged_transactions(service: TransactionServiceImpl = Depends(_service)):
    """Get all flagged/suspicious transactions for admin review."""
    return service.get_flagged_transactions()


@router.get("/user/{user_id}", response_model=list[TransactionResponse])
def get_transactions_by_user(
    user_id: int,
    service: TransactionServiceImpl = Depends(_service),
):
    """Admin views all transactions for a specific user."""
    return service.get_transactions_by_user_id(user_id)


@router.get("/{item_id}", response_model=TransactionResponse)
def get_transaction(item_id: int, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return item


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    repo: SQLAlchemyTransactionRepository = Depends(_repo),
):
    return repo.create(data)


@router.put("/{item_id}", response_model=TransactionResponse)
def update_transaction(
    item_id: int,
    data: TransactionUpdate,
    repo: SQLAlchemyTransactionRepository = Depends(_repo),
):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(item_id: int, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")