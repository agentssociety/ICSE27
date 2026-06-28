from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.patient_queue.patient_queue_dto import PatientQueueCreate, PatientQueueUpdate, PatientQueueResponse
from src.infra.patient_queue.patient_queue_repo_impl import SQLAlchemyPatientQueueRepository

"""
Api layer for the PatientQueue domain class

Package: api.patient_queue
Layer: api
Related tasks: #1, #3, #4, #5, #6
Requirement coverage:
- Register New Patient with Symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Dequeue Next Highest-Priority Patient
- Real-time Patient Dashboard
"""

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPatientQueueRepository:
    return SQLAlchemyPatientQueueRepository(db)


@router.get("", response_model=list[PatientQueueResponse])
def list_patient_queues(skip: int = 0, limit: int = 100, repo: SQLAlchemyPatientQueueRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=PatientQueueResponse)
def get_patient_queue(item_id: int, repo: SQLAlchemyPatientQueueRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientQueue not found")
    return item


@router.post("", response_model=PatientQueueResponse, status_code=status.HTTP_201_CREATED)
def create_patient_queue(data: PatientQueueCreate, repo: SQLAlchemyPatientQueueRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=PatientQueueResponse)
def update_patient_queue(item_id: int, data: PatientQueueUpdate, repo: SQLAlchemyPatientQueueRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientQueue not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_queue(item_id: int, repo: SQLAlchemyPatientQueueRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientQueue not found")
