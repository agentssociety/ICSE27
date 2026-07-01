from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.profile.profile_dto import ProfileCreate, ProfileUpdate, ProfileResponse
from src.infra.profile.profile_repo_impl import SQLAlchemyProfileRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyProfileRepository:
    return SQLAlchemyProfileRepository(db)


@router.get("", response_model=list[ProfileResponse])
def list_profiles(skip: int = 0, limit: int = 100, repo: SQLAlchemyProfileRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ProfileResponse)
def get_profile(item_id: int, repo: SQLAlchemyProfileRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return item


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(data: ProfileCreate, repo: SQLAlchemyProfileRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ProfileResponse)
def update_profile(item_id: int, data: ProfileUpdate, repo: SQLAlchemyProfileRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(item_id: int, repo: SQLAlchemyProfileRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
