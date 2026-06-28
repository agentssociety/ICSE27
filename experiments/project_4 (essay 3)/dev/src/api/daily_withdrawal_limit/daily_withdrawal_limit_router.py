from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.daily_withdrawal_limit.daily_withdrawal_limit_dto import DailyWithdrawalLimitCreateRequest, DailyWithdrawalLimitUpdateRequest, DailyWithdrawalLimitResponse
from src.infra.daily_withdrawal_limit.daily_withdrawal_limit_repo_impl import SQLAlchemyDailyWithdrawalLimitRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyDailyWithdrawalLimitRepository:
    return SQLAlchemyDailyWithdrawalLimitRepository(db)


@router.get("", response_model=list[DailyWithdrawalLimitResponse])
def list_daily_withdrawal_limits(skip: int = 0, limit: int = 100, repo: SQLAlchemyDailyWithdrawalLimitRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=DailyWithdrawalLimitResponse)
def get_daily_withdrawal_limit(item_id: int, repo: SQLAlchemyDailyWithdrawalLimitRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DailyWithdrawalLimit not found")
    return item


@router.post("", response_model=DailyWithdrawalLimitResponse, status_code=status.HTTP_201_CREATED)
def create_daily_withdrawal_limit(data: DailyWithdrawalLimitCreateRequest, repo: SQLAlchemyDailyWithdrawalLimitRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=DailyWithdrawalLimitResponse)
def update_daily_withdrawal_limit(item_id: int, data: DailyWithdrawalLimitUpdateRequest, repo: SQLAlchemyDailyWithdrawalLimitRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DailyWithdrawalLimit not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_withdrawal_limit(item_id: int, repo: SQLAlchemyDailyWithdrawalLimitRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DailyWithdrawalLimit not found")
