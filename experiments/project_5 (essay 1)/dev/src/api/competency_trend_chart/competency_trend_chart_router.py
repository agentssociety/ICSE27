from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.competency_trend_chart.competency_trend_chart_dto import CompetencyTrendChartCreate, CompetencyTrendChartUpdate, CompetencyTrendChartResponse
from src.infra.competency_trend_chart.competency_trend_chart_repo_impl import SQLAlchemyCompetencyTrendChartRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCompetencyTrendChartRepository:
    return SQLAlchemyCompetencyTrendChartRepository(db)


@router.get("", response_model=list[CompetencyTrendChartResponse])
def list_competency_trend_charts(skip: int = 0, limit: int = 100, repo: SQLAlchemyCompetencyTrendChartRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CompetencyTrendChartResponse)
def get_competency_trend_chart(item_id: int, repo: SQLAlchemyCompetencyTrendChartRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyTrendChart not found")
    return item


@router.post("", response_model=CompetencyTrendChartResponse, status_code=status.HTTP_201_CREATED)
def create_competency_trend_chart(data: CompetencyTrendChartCreate, repo: SQLAlchemyCompetencyTrendChartRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CompetencyTrendChartResponse)
def update_competency_trend_chart(item_id: int, data: CompetencyTrendChartUpdate, repo: SQLAlchemyCompetencyTrendChartRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyTrendChart not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competency_trend_chart(item_id: int, repo: SQLAlchemyCompetencyTrendChartRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CompetencyTrendChart not found")
