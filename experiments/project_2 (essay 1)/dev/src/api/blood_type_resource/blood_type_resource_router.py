from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.blood_type_resource.blood_type_resource_dto import BloodTypeResourceCreate, BloodTypeResourceUpdate, BloodTypeResourceResponse
from src.infra.blood_type_resource.blood_type_resource_repo_impl import SQLAlchemyBloodTypeResourceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBloodTypeResourceRepository:
    return SQLAlchemyBloodTypeResourceRepository(db)


@router.get("", response_model=list[BloodTypeResourceResponse])
def list_blood_type_resources(skip: int = 0, limit: int = 100, repo: SQLAlchemyBloodTypeResourceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BloodTypeResourceResponse)
def get_blood_type_resource(item_id: int, repo: SQLAlchemyBloodTypeResourceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodTypeResource not found")
    return item


@router.post("", response_model=BloodTypeResourceResponse, status_code=status.HTTP_201_CREATED)
def create_blood_type_resource(data: BloodTypeResourceCreate, repo: SQLAlchemyBloodTypeResourceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BloodTypeResourceResponse)
def update_blood_type_resource(item_id: int, data: BloodTypeResourceUpdate, repo: SQLAlchemyBloodTypeResourceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodTypeResource not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_type_resource(item_id: int, repo: SQLAlchemyBloodTypeResourceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BloodTypeResource not found")
