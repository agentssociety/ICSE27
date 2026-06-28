from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse
from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPatientRepository:
    return SQLAlchemyPatientRepository(db)


@router.get("", response_model=list[PatientResponse])
@router.get("/", response_model=list[PatientResponse])
def list_patients(skip: int = 0, limit: int = 100, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    patient = repo.get_by_id(patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(data: PatientCreate, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: str, data: PatientUpdate, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    patient = repo.update(patient_id, data)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


@router.delete("/{patient_id}", response_model=dict)
def delete_patient(patient_id: str, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    if not repo.delete(patient_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return {"message": "Patient deleted"}
