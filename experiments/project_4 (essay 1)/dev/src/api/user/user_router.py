from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.user.user_dto import UserCreate, UserUpdate, UserResponse
from src.infra.user.user_repo_impl import SQLAlchemyUserRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


@router.get("", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, repo: SQLAlchemyUserRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=UserResponse)
def get_user(item_id: int, repo: SQLAlchemyUserRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return item


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, repo: SQLAlchemyUserRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=UserResponse)
def update_user(item_id: int, data: UserUpdate, repo: SQLAlchemyUserRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(item_id: int, repo: SQLAlchemyUserRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
