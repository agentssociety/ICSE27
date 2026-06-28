from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.account_flag.account_flag_dto import AccountFlagCreate, AccountFlagUpdate, AccountFlagResponse
from src.infra.account_flag.account_flag_repo_impl import SQLAlchemyAccountFlagRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAccountFlagRepository:
    return SQLAlchemyAccountFlagRepository(db)


@router.get("", response_model=list[AccountFlagResponse])
def list_account_flags(skip: int = 0, limit: int = 100, repo: SQLAlchemyAccountFlagRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AccountFlagResponse)
def get_account_flag(item_id: int, repo: SQLAlchemyAccountFlagRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountFlag not found")
    return item


@router.post("", response_model=AccountFlagResponse, status_code=status.HTTP_201_CREATED)
def create_account_flag(data: AccountFlagCreate, repo: SQLAlchemyAccountFlagRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AccountFlagResponse)
def update_account_flag(item_id: int, data: AccountFlagUpdate, repo: SQLAlchemyAccountFlagRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountFlag not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_flag(item_id: int, repo: SQLAlchemyAccountFlagRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AccountFlag not found")