from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transaction_state_change.transaction_state_change_dto import TransactionStateChangeCreate, TransactionStateChangeUpdate, TransactionStateChangeResponse
from src.infra.transaction_state_change.transaction_state_change_repo_impl import SQLAlchemyTransactionStateChangeRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransactionStateChangeRepository:
    return SQLAlchemyTransactionStateChangeRepository(db)


@router.get("", response_model=list[TransactionStateChangeResponse])
def list_transaction_state_changes(skip: int = 0, limit: int = 100, repo: SQLAlchemyTransactionStateChangeRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TransactionStateChangeResponse)
def get_transaction_state_change(item_id: int, repo: SQLAlchemyTransactionStateChangeRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionStateChange not found")
    return item


@router.post("", response_model=TransactionStateChangeResponse, status_code=status.HTTP_201_CREATED)
def create_transaction_state_change(data: TransactionStateChangeCreate, repo: SQLAlchemyTransactionStateChangeRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TransactionStateChangeResponse)
def update_transaction_state_change(item_id: int, data: TransactionStateChangeUpdate, repo: SQLAlchemyTransactionStateChangeRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionStateChange not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_state_change(item_id: int, repo: SQLAlchemyTransactionStateChangeRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransactionStateChange not found")
