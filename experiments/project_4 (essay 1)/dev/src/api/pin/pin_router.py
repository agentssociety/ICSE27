from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.pin.pin_dto import PINCreate, PINUpdate, PINResponse
from src.infra.pin.pin_repo_impl import SQLAlchemyPINRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPINRepository:
    return SQLAlchemyPINRepository(db)


@router.get("", response_model=list[PINResponse])
def list_pins(skip: int = 0, limit: int = 100, repo: SQLAlchemyPINRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=PINResponse)
def get_pin(item_id: int, repo: SQLAlchemyPINRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PIN not found")
    return item


@router.post("", response_model=PINResponse, status_code=status.HTTP_201_CREATED)
def create_pin(data: PINCreate, repo: SQLAlchemyPINRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=PINResponse)
def update_pin(item_id: int, data: PINUpdate, repo: SQLAlchemyPINRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PIN not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pin(item_id: int, repo: SQLAlchemyPINRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PIN not found")