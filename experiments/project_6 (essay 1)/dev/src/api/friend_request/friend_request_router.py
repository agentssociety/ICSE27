from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.friend_request.friend_request_dto import FriendRequestCreate, FriendRequestUpdate, FriendRequestResponse
from src.infra.friend_request.friend_request_repo_impl import SQLAlchemyFriendRequestRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyFriendRequestRepository:
    return SQLAlchemyFriendRequestRepository(db)


@router.get("", response_model=list[FriendRequestResponse])
def list_friend_requests(skip: int = 0, limit: int = 100, repo: SQLAlchemyFriendRequestRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=FriendRequestResponse)
def get_friend_request(item_id: int, repo: SQLAlchemyFriendRequestRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FriendRequest not found")
    return item


@router.post("", response_model=FriendRequestResponse, status_code=status.HTTP_201_CREATED)
def create_friend_request(data: FriendRequestCreate, repo: SQLAlchemyFriendRequestRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=FriendRequestResponse)
def update_friend_request(item_id: int, data: FriendRequestUpdate, repo: SQLAlchemyFriendRequestRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FriendRequest not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_friend_request(item_id: int, repo: SQLAlchemyFriendRequestRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FriendRequest not found")
