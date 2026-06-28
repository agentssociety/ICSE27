from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.storage_state.storage_state_dto import StorageStateCreate, StorageStateUpdate, StorageStateResponse
from src.infra.storage_state.storage_state_repo_impl import SQLAlchemyStorageStateRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStorageStateRepository:
    return SQLAlchemyStorageStateRepository(db)


@router.get("", response_model=list[StorageStateResponse])
def list_storage_states(skip: int = 0, limit: int = 100, repo: SQLAlchemyStorageStateRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StorageStateResponse)
def get_storage_state(item_id: int, repo: SQLAlchemyStorageStateRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StorageState not found")
    return item


@router.post("", response_model=StorageStateResponse, status_code=status.HTTP_201_CREATED)
def create_storage_state(data: StorageStateCreate, repo: SQLAlchemyStorageStateRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StorageStateResponse)
def update_storage_state(item_id: int, data: StorageStateUpdate, repo: SQLAlchemyStorageStateRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StorageState not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_state(item_id: int, repo: SQLAlchemyStorageStateRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StorageState not found")
