from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.like.like_dto import LikeCreate, LikeUpdate, LikeResponse
from src.infra.like.like_repo_impl import SQLAlchemyLikeRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyLikeRepository:
    return SQLAlchemyLikeRepository(db)


@router.get("", response_model=list[LikeResponse])
def list_likes(skip: int = 0, limit: int = 100, repo: SQLAlchemyLikeRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=LikeResponse)
def get_like(item_id: int, repo: SQLAlchemyLikeRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return item


@router.post("", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def create_like(data: LikeCreate, repo: SQLAlchemyLikeRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=LikeResponse)
def update_like(item_id: int, data: LikeUpdate, repo: SQLAlchemyLikeRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_like(item_id: int, repo: SQLAlchemyLikeRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
