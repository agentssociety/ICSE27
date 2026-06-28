from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.account.account_dto import AccountCreateRequest, AccountUpdateRequest, AccountResponse
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAccountRepository:
    return SQLAlchemyAccountRepository(db)


@router.get("", response_model=list[AccountResponse])
def list_accounts(skip: int = 0, limit: int = 100, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AccountResponse)
def get_account(item_id: int, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return item


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(data: AccountCreateRequest, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AccountResponse)
def update_account(item_id: int, data: AccountUpdateRequest, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(item_id: int, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
