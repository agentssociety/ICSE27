from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.symptom_record.symptom_record_dto import SymptomRecordCreate, SymptomRecordUpdate, SymptomRecordResponse
from src.infra.symptom_record.symptom_record_repo_impl import SQLAlchemySymptomRecordRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySymptomRecordRepository:
    return SQLAlchemySymptomRecordRepository(db)


@router.get("", response_model=list[SymptomRecordResponse])
def list_symptom_records(skip: int = 0, limit: int = 100, repo: SQLAlchemySymptomRecordRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SymptomRecordResponse)
def get_symptom_record(item_id: int, repo: SQLAlchemySymptomRecordRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomRecord not found")
    return item


@router.post("", response_model=SymptomRecordResponse, status_code=status.HTTP_201_CREATED)
def create_symptom_record(data: SymptomRecordCreate, repo: SQLAlchemySymptomRecordRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SymptomRecordResponse)
def update_symptom_record(item_id: int, data: SymptomRecordUpdate, repo: SQLAlchemySymptomRecordRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomRecord not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom_record(item_id: int, repo: SQLAlchemySymptomRecordRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomRecord not found")
