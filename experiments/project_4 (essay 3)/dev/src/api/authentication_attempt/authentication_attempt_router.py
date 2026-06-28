from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.authentication_attempt.authentication_attempt_dto import AuthenticationAttemptCreate, AuthenticationAttemptResponse
from src.infra.authentication_attempt.authentication_attempt_repo_impl import SQLAlchemyAuthenticationAttemptRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuthenticationAttemptRepository:
    return SQLAlchemyAuthenticationAttemptRepository(db)


@router.get("", response_model=list[AuthenticationAttemptResponse])
def list_authentication_attempts(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuthenticationAttemptRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuthenticationAttemptResponse)
def get_authentication_attempt(item_id: str, repo: SQLAlchemyAuthenticationAttemptRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuthenticationAttempt not found")
    return item


@router.post("", response_model=AuthenticationAttemptResponse, status_code=status.HTTP_201_CREATED)
def create_authentication_attempt(data: AuthenticationAttemptCreate, repo: SQLAlchemyAuthenticationAttemptRepository = Depends(_repo)):
    return repo.create(data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_authentication_attempt(item_id: str, repo: SQLAlchemyAuthenticationAttemptRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuthenticationAttempt not found")
