from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.authentication_session.authentication_session_dto import AuthenticationSessionCreate, AuthenticationSessionUpdate, AuthenticationSessionResponse
from src.infra.authentication_session.authentication_session_repo_impl import SQLAlchemyAuthenticationSessionRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuthenticationSessionRepository:
    return SQLAlchemyAuthenticationSessionRepository(db)


@router.get("", response_model=list[AuthenticationSessionResponse])
def list_authentication_sessions(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuthenticationSessionRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuthenticationSessionResponse)
def get_authentication_session(item_id: int, repo: SQLAlchemyAuthenticationSessionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuthenticationSession not found")
    return item


@router.post("", response_model=AuthenticationSessionResponse, status_code=status.HTTP_201_CREATED)
def create_authentication_session(data: AuthenticationSessionCreate, repo: SQLAlchemyAuthenticationSessionRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AuthenticationSessionResponse)
def update_authentication_session(item_id: int, data: AuthenticationSessionUpdate, repo: SQLAlchemyAuthenticationSessionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuthenticationSession not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_authentication_session(item_id: int, repo: SQLAlchemyAuthenticationSessionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuthenticationSession not found")
