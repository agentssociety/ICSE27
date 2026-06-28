from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dto.patient_record.patient_record_dto import PatientRecordCreate, PatientRecordUpdate, PatientRecordResponse
from src.config.database import get_db
from src.infra.patient_record.patient_record_repo_impl import SQLAlchemyPatientRecordRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPatientRecordRepository:
    return SQLAlchemyPatientRecordRepository(db)

@router.get("", response_model=list[PatientRecordResponse])
def list_patient_records(skip: int = 0, limit: int = 100, repo: SQLAlchemyPatientRecordRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=PatientRecordResponse)
def get_patient_record(item_id: int, repo: SQLAlchemyPatientRecordRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientRecord not found")
    return item

@router.post("", response_model=PatientRecordResponse, status_code=status.HTTP_201_CREATED)
def create_patient_record(data: PatientRecordCreate, repo: SQLAlchemyPatientRecordRepository = Depends(_repo)):
    return repo.create(data)

@router.put("/{item_id}", response_model=PatientRecordResponse)
def update_patient_record(item_id: int, data: PatientRecordUpdate, repo: SQLAlchemyPatientRecordRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientRecord not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_record(item_id: int, repo: SQLAlchemyPatientRecordRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientRecord not found")