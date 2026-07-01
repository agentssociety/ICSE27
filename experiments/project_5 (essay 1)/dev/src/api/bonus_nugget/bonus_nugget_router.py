from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.bonus_nugget.bonus_nugget_dto import BonusNuggetCreate, BonusNuggetUpdate, BonusNuggetResponse
from src.infra.bonus_nugget.bonus_nugget_repo_impl import SQLAlchemyBonusNuggetRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBonusNuggetRepository:
    return SQLAlchemyBonusNuggetRepository(db)


@router.get("", response_model=list[BonusNuggetResponse])
def list_bonus_nuggets(skip: int = 0, limit: int = 100, repo: SQLAlchemyBonusNuggetRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BonusNuggetResponse)
def get_bonus_nugget(item_id: int, repo: SQLAlchemyBonusNuggetRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonusNugget not found")
    return item


@router.post("", response_model=BonusNuggetResponse, status_code=status.HTTP_201_CREATED)
def create_bonus_nugget(data: BonusNuggetCreate, repo: SQLAlchemyBonusNuggetRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BonusNuggetResponse)
def update_bonus_nugget(item_id: int, data: BonusNuggetUpdate, repo: SQLAlchemyBonusNuggetRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonusNugget not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bonus_nugget(item_id: int, repo: SQLAlchemyBonusNuggetRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonusNugget not found")
