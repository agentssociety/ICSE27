from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.blood_type.blood_type_dto import BloodTypeCreate, BloodTypeUpdate, BloodTypeResponse
from src.infra.blood_type.blood_type_repo_impl import SQLAlchemyBloodTypeRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBloodTypeRepository:
    return SQLAlchemyBloodTypeRepository(db)


@router.get("", response_model=list[BloodTypeResponse])
def list_blood_types(skip: int = 0, limit: int = 100, repo: SQLAlchemyBloodTypeRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BloodTypeResponse)
def get_blood_type(item_id: int, repo: SQLAlchemyBloodTypeRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodType not found")
    return item


@router.post("", response_model=BloodTypeResponse, status_code=status.HTTP_201_CREATED)
def create_blood_type(data: BloodTypeCreate, repo: SQLAlchemyBloodTypeRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BloodTypeResponse)
def update_blood_type(item_id: int, data: BloodTypeUpdate, repo: SQLAlchemyBloodTypeRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodType not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_type(item_id: int, repo: SQLAlchemyBloodTypeRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodType not found")
