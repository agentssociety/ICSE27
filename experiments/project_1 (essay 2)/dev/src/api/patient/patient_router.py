from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse, DashboardItem
from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository
from src.service.patient.patient_service import PatientServiceImpl

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPatientRepository:
    return SQLAlchemyPatientRepository(db)

def _svc(repo: SQLAlchemyPatientRepository = Depends(_repo)) -> PatientServiceImpl:
    return PatientServiceImpl(repository=repo)

@router.get("", response_model=list[PatientResponse])
def list_patients(skip: int = 0, limit: int = 100, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/dashboard", response_model=list[DashboardItem])
def get_dashboard(svc: PatientServiceImpl = Depends(_svc)):
    """Return dashboard data: each patient's urgency and estimated wait time."""
    queue = svc.get_sorted_queue()
    dashboard = []
    for position, patient in enumerate(queue):
        estimated_wait_minutes = (position + 1) * 10
        dashboard.append(DashboardItem(
            patient_id=patient.id,
            symptoms=patient.symptoms,
            urgency_level=patient.urgencyLevel,
            urgency=patient.urgency,
            queue_position=position + 1,
            estimated_wait_minutes=estimated_wait_minutes,
            arrival_time=patient.arrivalTime.isoformat(),
        ))
    return dashboard

@router.get("/{item_id}", response_model=PatientResponse)
def get_patient(item_id: int, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return item

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(data: PatientCreate, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    return repo.create(data)

@router.put("/{item_id}", response_model=PatientResponse)
def update_patient(item_id: int, data: PatientUpdate, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(item_id: int, repo: SQLAlchemyPatientRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
