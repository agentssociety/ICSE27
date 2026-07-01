from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.badge.badge_dto import BadgeCreate, BadgeUpdate, BadgeResponse
from src.infra.badge.badge_repo_impl import SQLAlchemyBadgeRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBadgeRepository:
    return SQLAlchemyBadgeRepository(db)


@router.get("", response_model=list[BadgeResponse])
def list_badges(skip: int = 0, limit: int = 100, repo: SQLAlchemyBadgeRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BadgeResponse)
def get_badge(item_id: str, repo: SQLAlchemyBadgeRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return item


@router.post("", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
def create_badge(data: BadgeCreate, repo: SQLAlchemyBadgeRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BadgeResponse)
def update_badge(item_id: str, data: BadgeUpdate, repo: SQLAlchemyBadgeRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(item_id: str, repo: SQLAlchemyBadgeRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
