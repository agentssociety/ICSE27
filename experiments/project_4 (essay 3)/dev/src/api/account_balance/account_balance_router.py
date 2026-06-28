from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.account_balance.account_balance_dto import AccountBalanceCreate, AccountBalanceUpdate, AccountBalanceResponse
from src.infra.account_balance.account_balance_repo_impl import SQLAlchemyAccountBalanceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAccountBalanceRepository:
    return SQLAlchemyAccountBalanceRepository(db)


@router.get("", response_model=list[AccountBalanceResponse])
def list_account_balances(skip: int = 0, limit: int = 100, repo: SQLAlchemyAccountBalanceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AccountBalanceResponse)
def get_account_balance(item_id: int, repo: SQLAlchemyAccountBalanceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountBalance not found")
    return item


@router.post("", response_model=AccountBalanceResponse, status_code=status.HTTP_201_CREATED)
def create_account_balance(data: AccountBalanceCreate, repo: SQLAlchemyAccountBalanceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AccountBalanceResponse)
def update_account_balance(item_id: int, data: AccountBalanceUpdate, repo: SQLAlchemyAccountBalanceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountBalance not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_balance(item_id: int, repo: SQLAlchemyAccountBalanceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountBalance not found")
