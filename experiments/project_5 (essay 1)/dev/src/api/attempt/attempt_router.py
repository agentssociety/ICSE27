from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.attempt.attempt_dto import AttemptCreate, AttemptUpdate, AttemptResponse
from src.infra.attempt.attempt_repo_impl import SQLAlchemyAttemptRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAttemptRepository:
    return SQLAlchemyAttemptRepository(db)


@router.get("", response_model=list[AttemptResponse])
def list_attempts(skip: int = 0, limit: int = 100, repo: SQLAlchemyAttemptRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AttemptResponse)
def get_attempt(item_id: int, repo: SQLAlchemyAttemptRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    return item


@router.post("", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
def create_attempt(data: AttemptCreate, repo: SQLAlchemyAttemptRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AttemptResponse)
def update_attempt(item_id: int, data: AttemptUpdate, repo: SQLAlchemyAttemptRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attempt(item_id: int, repo: SQLAlchemyAttemptRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
