from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.competency_breakdown.competency_breakdown_dto import CompetencyBreakdownCreate, CompetencyBreakdownUpdate, CompetencyBreakdownResponse
from src.infra.competency_breakdown.competency_breakdown_repo_impl import SQLAlchemyCompetencyBreakdownRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCompetencyBreakdownRepository:
    return SQLAlchemyCompetencyBreakdownRepository(db)


@router.get("", response_model=list[CompetencyBreakdownResponse])
def list_breakdowns(skip: int = 0, limit: int = 100, exam_session_id: Optional[int] = None,
                    repo: SQLAlchemyCompetencyBreakdownRepository = Depends(_repo)):
    if exam_session_id is not None:
        return repo.get_by_session(exam_session_id)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CompetencyBreakdownResponse)
def get_breakdown(item_id: int, repo: SQLAlchemyCompetencyBreakdownRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyBreakdown not found")
    return item


@router.post("", response_model=CompetencyBreakdownResponse, status_code=status.HTTP_201_CREATED)
def create_breakdown(data: CompetencyBreakdownCreate, repo: SQLAlchemyCompetencyBreakdownRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CompetencyBreakdownResponse)
def update_breakdown(item_id: int, data: CompetencyBreakdownUpdate, repo: SQLAlchemyCompetencyBreakdownRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyBreakdown not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breakdown(item_id: int, repo: SQLAlchemyCompetencyBreakdownRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyBreakdown not found")
