from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.state.state_dto import StateCreate, StateUpdate, StateResponse
from src.infra.state.state_repo_impl import SQLAlchemyStateRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStateRepository:
    return SQLAlchemyStateRepository(db)


@router.get("", response_model=list[StateResponse])
def list_states(skip: int = 0, limit: int = 100, repo: SQLAlchemyStateRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StateResponse)
def get_state(item_id: int, repo: SQLAlchemyStateRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return item


@router.post("", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
def create_state(data: StateCreate, repo: SQLAlchemyStateRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StateResponse)
def update_state(item_id: int, data: StateUpdate, repo: SQLAlchemyStateRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_state(item_id: int, repo: SQLAlchemyStateRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
