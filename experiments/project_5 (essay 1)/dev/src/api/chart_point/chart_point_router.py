from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.chart_point.chart_point_dto import ChartPointCreate, ChartPointUpdate, ChartPointResponse
from src.infra.chart_point.chart_point_repo_impl import SQLAlchemyChartPointRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyChartPointRepository:
    return SQLAlchemyChartPointRepository(db)


@router.get("", response_model=list[ChartPointResponse])
def list_chart_points(skip: int = 0, limit: int = 100, repo: SQLAlchemyChartPointRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ChartPointResponse)
def get_chart_point(item_id: int, repo: SQLAlchemyChartPointRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChartPoint not found")
    return item


@router.post("", response_model=ChartPointResponse, status_code=status.HTTP_201_CREATED)
def create_chart_point(data: ChartPointCreate, repo: SQLAlchemyChartPointRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ChartPointResponse)
def update_chart_point(item_id: int, data: ChartPointUpdate, repo: SQLAlchemyChartPointRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChartPoint not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chart_point(item_id: int, repo: SQLAlchemyChartPointRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChartPoint not found")
