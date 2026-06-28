from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.failed_attempt.failed_attempt_dto import FailedAttemptCreate, FailedAttemptUpdate, FailedAttemptResponse
from src.infra.failed_attempt.failed_attempt_repo_impl import SQLAlchemyFailedAttemptRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyFailedAttemptRepository:
    return SQLAlchemyFailedAttemptRepository(db)


@router.get("", response_model=list[FailedAttemptResponse])
def list_failed_attempts(skip: int = 0, limit: int = 100, repo: SQLAlchemyFailedAttemptRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=FailedAttemptResponse)
def get_failed_attempt(item_id: int, repo: SQLAlchemyFailedAttemptRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FailedAttempt not found")
    return item


@router.post("", response_model=FailedAttemptResponse, status_code=status.HTTP_201_CREATED)
def create_failed_attempt(data: FailedAttemptCreate, repo: SQLAlchemyFailedAttemptRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=FailedAttemptResponse)
def update_failed_attempt(item_id: int, data: FailedAttemptUpdate, repo: SQLAlchemyFailedAttemptRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FailedAttempt not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_failed_attempt(item_id: int, repo: SQLAlchemyFailedAttemptRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FailedAttempt not found")
