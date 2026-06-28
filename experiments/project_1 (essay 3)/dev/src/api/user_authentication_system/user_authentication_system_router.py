from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.user_authentication_system.user_authentication_system_dto import UserAuthenticationSystemCreate, UserAuthenticationSystemUpdate, UserAuthenticationSystemResponse
from src.infra.user_authentication_system.user_authentication_system_repo_impl import SQLAlchemyUserAuthenticationSystemRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyUserAuthenticationSystemRepository:
    return SQLAlchemyUserAuthenticationSystemRepository(db)


@router.get("", response_model=list[UserAuthenticationSystemResponse])
def list_user_authentication_systems(skip: int = 0, limit: int = 100, repo: SQLAlchemyUserAuthenticationSystemRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=UserAuthenticationSystemResponse)
def get_user_authentication_system(item_id: int, repo: SQLAlchemyUserAuthenticationSystemRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserAuthenticationSystem not found")
    return item


@router.post("", response_model=UserAuthenticationSystemResponse, status_code=status.HTTP_201_CREATED)
def create_user_authentication_system(data: UserAuthenticationSystemCreate, repo: SQLAlchemyUserAuthenticationSystemRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=UserAuthenticationSystemResponse)
def update_user_authentication_system(item_id: int, data: UserAuthenticationSystemUpdate, repo: SQLAlchemyUserAuthenticationSystemRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserAuthenticationSystem not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_authentication_system(item_id: int, repo: SQLAlchemyUserAuthenticationSystemRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserAuthenticationSystem not found")
