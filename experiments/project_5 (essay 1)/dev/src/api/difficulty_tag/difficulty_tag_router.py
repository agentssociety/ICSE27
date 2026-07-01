from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.difficulty_tag.difficulty_tag_dto import DifficultyTagCreate, DifficultyTagUpdate, DifficultyTagResponse
from src.infra.difficulty_tag.difficulty_tag_repo_impl import SQLAlchemyDifficultyTagRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyDifficultyTagRepository:
    return SQLAlchemyDifficultyTagRepository(db)


@router.get("", response_model=list[DifficultyTagResponse])
def list_difficulty_tags(skip: int = 0, limit: int = 100, repo: SQLAlchemyDifficultyTagRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=DifficultyTagResponse)
def get_difficulty_tag(item_id: int, repo: SQLAlchemyDifficultyTagRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DifficultyTag not found")
    return item


@router.post("", response_model=DifficultyTagResponse, status_code=status.HTTP_201_CREATED)
def create_difficulty_tag(data: DifficultyTagCreate, repo: SQLAlchemyDifficultyTagRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=DifficultyTagResponse)
def update_difficulty_tag(item_id: int, data: DifficultyTagUpdate, repo: SQLAlchemyDifficultyTagRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DifficultyTag not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_difficulty_tag(item_id: int, repo: SQLAlchemyDifficultyTagRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DifficultyTag not found")
