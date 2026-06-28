from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.lockout_record.lockout_record_dto import LockoutRecordCreate, LockoutRecordUpdate, LockoutRecordResponse
from src.infra.lockout_record.lockout_record_repo_impl import SQLAlchemyLockoutRecordRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyLockoutRecordRepository:
    return SQLAlchemyLockoutRecordRepository(db)


@router.get("", response_model=list[LockoutRecordResponse])
def list_lockout_records(skip: int = 0, limit: int = 100, repo: SQLAlchemyLockoutRecordRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=LockoutRecordResponse)
def get_lockout_record(item_id: int, repo: SQLAlchemyLockoutRecordRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutRecord not found")
    return item


@router.post("", response_model=LockoutRecordResponse, status_code=status.HTTP_201_CREATED)
def create_lockout_record(data: LockoutRecordCreate, repo: SQLAlchemyLockoutRecordRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=LockoutRecordResponse)
def update_lockout_record(item_id: int, data: LockoutRecordUpdate, repo: SQLAlchemyLockoutRecordRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutRecord not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lockout_record(item_id: int, repo: SQLAlchemyLockoutRecordRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutRecord not found")
