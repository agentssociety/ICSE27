from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.avatar.avatar_dto import AvatarCreate, AvatarUpdate, AvatarResponse
from src.infra.avatar.avatar_repo_impl import SQLAlchemyAvatarRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAvatarRepository:
    return SQLAlchemyAvatarRepository(db)


@router.get("", response_model=list[AvatarResponse])
def list_avatars(skip: int = 0, limit: int = 100, repo: SQLAlchemyAvatarRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AvatarResponse)
def get_avatar(item_id: int, repo: SQLAlchemyAvatarRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    return item


@router.post("", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
def create_avatar(data: AvatarCreate, repo: SQLAlchemyAvatarRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AvatarResponse)
def update_avatar(item_id: int, data: AvatarUpdate, repo: SQLAlchemyAvatarRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(item_id: int, repo: SQLAlchemyAvatarRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
