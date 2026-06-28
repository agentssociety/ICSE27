from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.symptom_data.symptom_data_dto import SymptomDataCreate, SymptomDataUpdate, SymptomDataResponse
from src.infra.symptom_data.symptom_data_repo_impl import SQLAlchemySymptomDataRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemySymptomDataRepository:
    return SQLAlchemySymptomDataRepository(db)

@router.get("", response_model=list[SymptomDataResponse])
def list_symptom_datas(skip: int = 0, limit: int = 100, repo: SQLAlchemySymptomDataRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=SymptomDataResponse)
def get_symptom_data(item_id: int, repo: SQLAlchemySymptomDataRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomData not found")
    return item

@router.post("", response_model=SymptomDataResponse, status_code=status.HTTP_201_CREATED)
def create_symptom_data(data: SymptomDataCreate, repo: SQLAlchemySymptomDataRepository = Depends(_repo)):
    return repo.create(data)

@router.put("/{item_id}", response_model=SymptomDataResponse)
def update_symptom_data(item_id: int, data: SymptomDataUpdate, repo: SQLAlchemySymptomDataRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomData not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom_data(item_id: int, repo: SQLAlchemySymptomDataRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SymptomData not found")