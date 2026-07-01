from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.friendship.friendship_dto import FriendshipCreate, FriendshipUpdate, FriendshipResponse
from src.infra.friendship.friendship_repo_impl import SQLAlchemyFriendshipRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyFriendshipRepository:
    return SQLAlchemyFriendshipRepository(db)


@router.get("", response_model=list[FriendshipResponse])
def list_friendships(skip: int = 0, limit: int = 100, repo: SQLAlchemyFriendshipRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=FriendshipResponse)
def get_friendship(item_id: int, repo: SQLAlchemyFriendshipRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
    return item


@router.post("", response_model=FriendshipResponse, status_code=status.HTTP_201_CREATED)
def create_friendship(data: FriendshipCreate, repo: SQLAlchemyFriendshipRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=FriendshipResponse)
def update_friendship(item_id: int, data: FriendshipUpdate, repo: SQLAlchemyFriendshipRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_friendship(item_id: int, repo: SQLAlchemyFriendshipRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
