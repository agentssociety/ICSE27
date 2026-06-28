from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.time_slot.time_slot_dto import TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse
from src.infra.time_slot.time_slot_repo_impl import SQLAlchemyTimeSlotRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTimeSlotRepository:
    return SQLAlchemyTimeSlotRepository(db)


@router.get("", response_model=list[TimeSlotResponse])
def list_time_slots(skip: int = 0, limit: int = 100, repo: SQLAlchemyTimeSlotRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TimeSlotResponse)
def get_time_slot(item_id: int, repo: SQLAlchemyTimeSlotRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found")
    return item


@router.post("", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
def create_time_slot(data: TimeSlotCreate, repo: SQLAlchemyTimeSlotRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TimeSlotResponse)
def update_time_slot(item_id: int, data: TimeSlotUpdate, repo: SQLAlchemyTimeSlotRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_slot(item_id: int, repo: SQLAlchemyTimeSlotRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found")
