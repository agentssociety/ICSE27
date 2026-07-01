from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.schedule.schedule_dto import ScheduleCreateRequest, ScheduleUpdateRequest, ScheduleResponse
from src.infra.schedule.schedule_repo_impl import SQLAlchemyScheduleRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyScheduleRepository:
    return SQLAlchemyScheduleRepository(db)


@router.get("", response_model=list[ScheduleResponse])
def list_schedules(skip: int = 0, limit: int = 100, repo: SQLAlchemyScheduleRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ScheduleResponse)
def get_schedule(item_id: int, repo: SQLAlchemyScheduleRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return item


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(data: ScheduleCreateRequest, repo: SQLAlchemyScheduleRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ScheduleResponse)
def update_schedule(item_id: int, data: ScheduleUpdateRequest, repo: SQLAlchemyScheduleRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(item_id: int, repo: SQLAlchemyScheduleRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
