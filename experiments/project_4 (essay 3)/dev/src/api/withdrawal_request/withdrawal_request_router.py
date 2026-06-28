from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.withdrawal_request.withdrawal_request_dto import WithdrawalRequestCreate, WithdrawalRequestUpdate, WithdrawalRequestResponse
from src.infra.withdrawal_request.withdrawal_request_repo_impl import SQLAlchemyWithdrawalRequestRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalRequestRepository:
    return SQLAlchemyWithdrawalRequestRepository(db)


@router.get("", response_model=list[WithdrawalRequestResponse])
def list_withdrawal_requests(skip: int = 0, limit: int = 100, repo: SQLAlchemyWithdrawalRequestRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=WithdrawalRequestResponse)
def get_withdrawal_request(item_id: int, repo: SQLAlchemyWithdrawalRequestRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRequest not found")
    return item


@router.post("", response_model=WithdrawalRequestResponse, status_code=status.HTTP_201_CREATED)
def create_withdrawal_request(data: WithdrawalRequestCreate, repo: SQLAlchemyWithdrawalRequestRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=WithdrawalRequestResponse)
def update_withdrawal_request(item_id: int, data: WithdrawalRequestUpdate, repo: SQLAlchemyWithdrawalRequestRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRequest not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_withdrawal_request(item_id: int, repo: SQLAlchemyWithdrawalRequestRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRequest not found")
