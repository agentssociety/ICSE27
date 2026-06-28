from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.symptom.symptom_dto import SymptomCreate, SymptomUpdate, SymptomResponse
from src.infra.symptom.symptom_repo_impl import SQLAlchemySymptomRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySymptomRepository:
    return SQLAlchemySymptomRepository(db)


@router.get("", response_model=list[SymptomResponse])
def list_symptoms(skip: int = 0, limit: int = 100, repo: SQLAlchemySymptomRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SymptomResponse)
def get_symptom(item_id: int, repo: SQLAlchemySymptomRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom not found")
    return item


@router.post("", response_model=SymptomResponse, status_code=status.HTTP_201_CREATED)
def create_symptom(data: SymptomCreate, repo: SQLAlchemySymptomRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SymptomResponse)
def update_symptom(item_id: int, data: SymptomUpdate, repo: SQLAlchemySymptomRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom(item_id: int, repo: SQLAlchemySymptomRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Symptom not found")
