from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.reward_item.reward_item_dto import RewardItemCreate, RewardItemUpdate, RewardItemResponse
from src.infra.reward_item.reward_item_repo_impl import SQLAlchemyRewardItemRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRewardItemRepository:
    return SQLAlchemyRewardItemRepository(db)


@router.get("", response_model=list[RewardItemResponse])
def list_items(skip: int = 0, limit: int = 100, repo: SQLAlchemyRewardItemRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RewardItemResponse)
def get_item(item_id: int, repo: SQLAlchemyRewardItemRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardItem not found")
    return item


@router.post("", response_model=RewardItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(data: RewardItemCreate, repo: SQLAlchemyRewardItemRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RewardItemResponse)
def update_item(item_id: int, data: RewardItemUpdate, repo: SQLAlchemyRewardItemRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardItem not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, repo: SQLAlchemyRewardItemRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardItem not found")
