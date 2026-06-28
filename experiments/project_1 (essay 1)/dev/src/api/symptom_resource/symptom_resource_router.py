from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.symptom_resource.symptom_resource_dto import SymptomResourceCreate, SymptomResourceUpdate, SymptomResourceResponse
from src.infra.symptom_resource.symptom_resource_repo_impl import SQLAlchemySymptomResourceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySymptomResourceRepository:
    return SQLAlchemySymptomResourceRepository(db)


@router.get("", response_model=list[SymptomResourceResponse])
def list_symptom_resources(skip: int = 0, limit: int = 100, repo: SQLAlchemySymptomResourceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SymptomResourceResponse)
def get_symptom_resource(item_id: int, repo: SQLAlchemySymptomResourceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomResource not found")
    return item


@router.post("", response_model=SymptomResourceResponse, status_code=status.HTTP_201_CREATED)
def create_symptom_resource(data: SymptomResourceCreate, repo: SQLAlchemySymptomResourceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SymptomResourceResponse)
def update_symptom_resource(item_id: int, data: SymptomResourceUpdate, repo: SQLAlchemySymptomResourceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomResource not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom_resource(item_id: int, repo: SQLAlchemySymptomResourceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomResource not found")
