from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transaction.transaction_dto import TransactionCreateRequest, TransactionUpdateRequest, TransactionResponse
from src.infra.transaction.transaction_repo_impl import SQLAlchemyTransactionRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransactionRepository:
    return SQLAlchemyTransactionRepository(db)


@router.get("", response_model=list[TransactionResponse])
def list_transactions(skip: int = 0, limit: int = 100, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TransactionResponse)
def get_transaction(item_id: str, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return item


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(data: TransactionCreateRequest, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TransactionResponse)
def update_transaction(item_id: str, data: TransactionUpdateRequest, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(item_id: str, repo: SQLAlchemyTransactionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")


class TransactionRouter:
    def __init__(self) -> None:
        pass
