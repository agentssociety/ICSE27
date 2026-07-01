from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.saved_list.saved_list_dto import SavedListCreate, SavedListUpdate, SavedListResponse
from src.infra.saved_list.saved_list_repo_impl import SQLAlchemySavedListRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySavedListRepository:
    return SQLAlchemySavedListRepository(db)


@router.get("", response_model=list[SavedListResponse])
def list_saved_lists(skip: int = 0, limit: int = 100, repo: SQLAlchemySavedListRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SavedListResponse)
def get_saved_list(item_id: int, repo: SQLAlchemySavedListRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SavedList not found")
    return item


@router.post("", response_model=SavedListResponse, status_code=status.HTTP_201_CREATED)
def create_saved_list(data: SavedListCreate, repo: SQLAlchemySavedListRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SavedListResponse)
def update_saved_list(item_id: int, data: SavedListUpdate, repo: SQLAlchemySavedListRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SavedList not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_list(item_id: int, repo: SQLAlchemySavedListRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SavedList not found")
