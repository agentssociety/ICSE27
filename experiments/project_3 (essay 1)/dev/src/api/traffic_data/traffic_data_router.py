from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.traffic_data.traffic_data_dto import TrafficDataCreate, TrafficDataUpdate, TrafficDataResponse
from src.infra.traffic_data.traffic_data_repo_impl import SQLAlchemyTrafficDataRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTrafficDataRepository:
    return SQLAlchemyTrafficDataRepository(db)


@router.get("", response_model=list[TrafficDataResponse])
def list_traffic_datas(skip: int = 0, limit: int = 100, repo: SQLAlchemyTrafficDataRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TrafficDataResponse)
def get_traffic_data(item_id: int, repo: SQLAlchemyTrafficDataRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TrafficData not found")
    return item


@router.post("", response_model=TrafficDataResponse, status_code=status.HTTP_201_CREATED)
def create_traffic_data(data: TrafficDataCreate, repo: SQLAlchemyTrafficDataRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TrafficDataResponse)
def update_traffic_data(item_id: int, data: TrafficDataUpdate, repo: SQLAlchemyTrafficDataRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TrafficData not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_traffic_data(item_id: int, repo: SQLAlchemyTrafficDataRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TrafficData not found")
