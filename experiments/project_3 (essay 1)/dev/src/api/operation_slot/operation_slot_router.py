from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.operation_slot.operation_slot_dto import OperationSlotCreate, OperationSlotUpdate, OperationSlotResponse
from src.infra.operation_slot.operation_slot_repo_impl import SQLAlchemyOperationSlotRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyOperationSlotRepository:
    return SQLAlchemyOperationSlotRepository(db)


@router.get("", response_model=list[OperationSlotResponse])
def list_operation_slots(skip: int = 0, limit: int = 100, repo: SQLAlchemyOperationSlotRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=OperationSlotResponse)
def get_operation_slot(item_id: int, repo: SQLAlchemyOperationSlotRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OperationSlot not found")
    return item


@router.post("", response_model=OperationSlotResponse, status_code=status.HTTP_201_CREATED)
def create_operation_slot(data: OperationSlotCreate, repo: SQLAlchemyOperationSlotRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=OperationSlotResponse)
def update_operation_slot(item_id: int, data: OperationSlotUpdate, repo: SQLAlchemyOperationSlotRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OperationSlot not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation_slot(item_id: int, repo: SQLAlchemyOperationSlotRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OperationSlot not found")
