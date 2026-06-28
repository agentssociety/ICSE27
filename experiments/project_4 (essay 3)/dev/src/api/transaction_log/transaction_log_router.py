from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transaction_log.transaction_log_dto import TransactionLogCreate, TransactionLogUpdate, TransactionLogResponse
from src.infra.transaction_log.transaction_log_repo_impl import SQLAlchemyTransactionLogRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransactionLogRepository:
    return SQLAlchemyTransactionLogRepository(db)


@router.get("", response_model=list[TransactionLogResponse])
def list_transaction_logs(skip: int = 0, limit: int = 100, repo: SQLAlchemyTransactionLogRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TransactionLogResponse)
def get_transaction_log(item_id: int, repo: SQLAlchemyTransactionLogRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionLog not found")
    return item


@router.post("", response_model=TransactionLogResponse, status_code=status.HTTP_201_CREATED)
def create_transaction_log(data: TransactionLogCreate, repo: SQLAlchemyTransactionLogRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TransactionLogResponse)
def update_transaction_log(item_id: int, data: TransactionLogUpdate, repo: SQLAlchemyTransactionLogRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionLog not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_log(item_id: int, repo: SQLAlchemyTransactionLogRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionLog not found")
