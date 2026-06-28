from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.withdrawal_record.withdrawal_record_dto import WithdrawalRecordCreate, WithdrawalRecordUpdate, WithdrawalRecordResponse
from src.infra.withdrawal_record.withdrawal_record_repo_impl import SQLAlchemyWithdrawalRecordRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalRecordRepository:
    return SQLAlchemyWithdrawalRecordRepository(db)


@router.get("", response_model=list[WithdrawalRecordResponse])
def list_withdrawal_records(skip: int = 0, limit: int = 100, repo: SQLAlchemyWithdrawalRecordRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=WithdrawalRecordResponse)
def get_withdrawal_record(item_id: int, repo: SQLAlchemyWithdrawalRecordRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRecord not found")
    return item


@router.post("", response_model=WithdrawalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_withdrawal_record(data: WithdrawalRecordCreate, repo: SQLAlchemyWithdrawalRecordRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=WithdrawalRecordResponse)
def update_withdrawal_record(item_id: int, data: WithdrawalRecordUpdate, repo: SQLAlchemyWithdrawalRecordRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRecord not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_withdrawal_record(item_id: int, repo: SQLAlchemyWithdrawalRecordRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WithdrawalRecord not found")
