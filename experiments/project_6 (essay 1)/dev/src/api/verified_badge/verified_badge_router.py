from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.verified_badge.verified_badge_dto import VerifiedBadgeCreate, VerifiedBadgeUpdate, VerifiedBadgeResponse
from src.infra.verified_badge.verified_badge_repo_impl import SQLAlchemyVerifiedBadgeRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyVerifiedBadgeRepository:
    return SQLAlchemyVerifiedBadgeRepository(db)


@router.get("", response_model=list[VerifiedBadgeResponse])
def list_verified_badges(skip: int = 0, limit: int = 100, repo: SQLAlchemyVerifiedBadgeRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=VerifiedBadgeResponse)
def get_verified_badge(item_id: int, repo: SQLAlchemyVerifiedBadgeRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VerifiedBadge not found")
    return item


@router.post("", response_model=VerifiedBadgeResponse, status_code=status.HTTP_201_CREATED)
def create_verified_badge(data: VerifiedBadgeCreate, repo: SQLAlchemyVerifiedBadgeRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=VerifiedBadgeResponse)
def update_verified_badge(item_id: int, data: VerifiedBadgeUpdate, repo: SQLAlchemyVerifiedBadgeRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VerifiedBadge not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_verified_badge(item_id: int, repo: SQLAlchemyVerifiedBadgeRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VerifiedBadge not found")
