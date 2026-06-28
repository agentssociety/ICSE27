from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.withdrawal_limit.withdrawal_limit_dto import WithdrawalLimitCreate, WithdrawalLimitUpdate, WithdrawalLimitResponse
from src.infra.withdrawal_limit.withdrawal_limit_repo_impl import SQLAlchemyWithdrawalLimitRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalLimitRepository:
    return SQLAlchemyWithdrawalLimitRepository(db)


@router.get("", response_model=list[WithdrawalLimitResponse])
def list_withdrawal_limits(skip: int = 0, limit: int = 100, repo: SQLAlchemyWithdrawalLimitRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=WithdrawalLimitResponse)
def get_withdrawal_limit(item_id: int, repo: SQLAlchemyWithdrawalLimitRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalLimit not found")
    return item


@router.post("", response_model=WithdrawalLimitResponse, status_code=status.HTTP_201_CREATED)
def create_withdrawal_limit(data: WithdrawalLimitCreate, repo: SQLAlchemyWithdrawalLimitRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=WithdrawalLimitResponse)
def update_withdrawal_limit(item_id: int, data: WithdrawalLimitUpdate, repo: SQLAlchemyWithdrawalLimitRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalLimit not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_withdrawal_limit(item_id: int, repo: SQLAlchemyWithdrawalLimitRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalLimit not found")
