from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.slot.slot_dto import SlotCreate, SlotUpdate, SlotResponse
from src.infra.slot.slot_repo_impl import SQLAlchemySlotRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySlotRepository:
    return SQLAlchemySlotRepository(db)


@router.get("", response_model=list[SlotResponse])
def list_slots(skip: int = 0, limit: int = 100, repo: SQLAlchemySlotRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SlotResponse)
def get_slot(item_id: int, repo: SQLAlchemySlotRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    return item


@router.post("", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(data: SlotCreate, repo: SQLAlchemySlotRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SlotResponse)
def update_slot(item_id: int, data: SlotUpdate, repo: SQLAlchemySlotRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(item_id: int, repo: SQLAlchemySlotRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
