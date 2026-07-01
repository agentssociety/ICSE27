from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.cohort_leaderboard.cohort_leaderboard_dto import CohortLeaderboardCreate, CohortLeaderboardUpdate, CohortLeaderboardResponse
from src.infra.cohort_leaderboard.cohort_leaderboard_repo_impl import SQLAlchemyCohortLeaderboardRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCohortLeaderboardRepository:
    return SQLAlchemyCohortLeaderboardRepository(db)


@router.get("", response_model=list[CohortLeaderboardResponse])
def list_cohort_leaderboards(skip: int = 0, limit: int = 100, repo: SQLAlchemyCohortLeaderboardRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CohortLeaderboardResponse)
def get_cohort_leaderboard(item_id: int, repo: SQLAlchemyCohortLeaderboardRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CohortLeaderboard not found")
    return item


@router.post("", response_model=CohortLeaderboardResponse, status_code=status.HTTP_201_CREATED)
def create_cohort_leaderboard(data: CohortLeaderboardCreate, repo: SQLAlchemyCohortLeaderboardRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CohortLeaderboardResponse)
def update_cohort_leaderboard(item_id: int, data: CohortLeaderboardUpdate, repo: SQLAlchemyCohortLeaderboardRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CohortLeaderboard not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cohort_leaderboard(item_id: int, repo: SQLAlchemyCohortLeaderboardRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CohortLeaderboard not found")
