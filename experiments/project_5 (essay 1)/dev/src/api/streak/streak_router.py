from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.streak.streak_dto import StreakCreate, StreakUpdate, StreakResponse
from src.infra.streak.streak_repo_impl import SQLAlchemyStreakRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStreakRepository:
    return SQLAlchemyStreakRepository(db)


@router.get("", response_model=list[StreakResponse])
def list_streaks(skip: int = 0, limit: int = 100, student_id: Optional[int] = None,
                 repo: SQLAlchemyStreakRepository = Depends(_repo)):
    if student_id is not None:
        item = repo.get_by_student_id(student_id)
        return [item] if item else []
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StreakResponse)
def get_streak(item_id: int, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Streak not found")
    return item


@router.post("", response_model=StreakResponse, status_code=status.HTTP_201_CREATED)
def create_streak(data: StreakCreate, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StreakResponse)
def update_streak(item_id: int, data: StreakUpdate, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Streak not found")
    return item


@router.post("/{item_id}/correct", response_model=StreakResponse)
def record_correct(item_id: int, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    row = repo.get_by_id(item_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Streak not found")
    result = repo.record_correct(row.student_id)
    return result


@router.post("/{item_id}/wrong", response_model=StreakResponse)
def record_wrong(item_id: int, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    row = repo.get_by_id(item_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Streak not found")
    result = repo.record_wrong(row.student_id)
    return result


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_streak(item_id: int, repo: SQLAlchemyStreakRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Streak not found")
