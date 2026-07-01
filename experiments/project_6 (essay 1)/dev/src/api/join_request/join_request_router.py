from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.join_request.join_request_dto import JoinRequestCreate, JoinRequestUpdate, JoinRequestResponse
from src.infra.join_request.join_request_repo_impl import SQLAlchemyJoinRequestRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyJoinRequestRepository:
    return SQLAlchemyJoinRequestRepository(db)


@router.get("", response_model=list[JoinRequestResponse])
def list_join_requests(skip: int = 0, limit: int = 100, repo: SQLAlchemyJoinRequestRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=JoinRequestResponse)
def get_join_request(item_id: int, repo: SQLAlchemyJoinRequestRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JoinRequest not found")
    return item


@router.post("", response_model=JoinRequestResponse, status_code=status.HTTP_201_CREATED)
def create_join_request(data: JoinRequestCreate, repo: SQLAlchemyJoinRequestRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=JoinRequestResponse)
def update_join_request(item_id: int, data: JoinRequestUpdate, repo: SQLAlchemyJoinRequestRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JoinRequest not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_join_request(item_id: int, repo: SQLAlchemyJoinRequestRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="JoinRequest not found")
