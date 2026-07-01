from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.radar_chart.radar_chart_dto import RadarChartCreate, RadarChartUpdate, RadarChartResponse
from src.infra.radar_chart.radar_chart_repo_impl import SQLAlchemyRadarChartRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRadarChartRepository:
    return SQLAlchemyRadarChartRepository(db)


@router.get("", response_model=list[RadarChartResponse])
def list_radar_charts(skip: int = 0, limit: int = 100, repo: SQLAlchemyRadarChartRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RadarChartResponse)
def get_radar_chart(item_id: int, repo: SQLAlchemyRadarChartRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RadarChart not found")
    return item


@router.post("", response_model=RadarChartResponse, status_code=status.HTTP_201_CREATED)
def create_radar_chart(data: RadarChartCreate, repo: SQLAlchemyRadarChartRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RadarChartResponse)
def update_radar_chart(item_id: int, data: RadarChartUpdate, repo: SQLAlchemyRadarChartRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RadarChart not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_radar_chart(item_id: int, repo: SQLAlchemyRadarChartRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RadarChart not found")
