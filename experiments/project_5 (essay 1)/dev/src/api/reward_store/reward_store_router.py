from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.reward_store.reward_store_dto import RewardStoreCreate, RewardStoreUpdate, RewardStoreResponse
from src.infra.reward_store.reward_store_repo_impl import SQLAlchemyRewardStoreRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRewardStoreRepository:
    return SQLAlchemyRewardStoreRepository(db)


@router.get("", response_model=list[RewardStoreResponse])
def list_stores(skip: int = 0, limit: int = 100, repo: SQLAlchemyRewardStoreRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RewardStoreResponse)
def get_store(item_id: int, repo: SQLAlchemyRewardStoreRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardStore not found")
    return item


@router.post("", response_model=RewardStoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(data: RewardStoreCreate, repo: SQLAlchemyRewardStoreRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RewardStoreResponse)
def update_store(item_id: int, data: RewardStoreUpdate, repo: SQLAlchemyRewardStoreRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardStore not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(item_id: int, repo: SQLAlchemyRewardStoreRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardStore not found")
