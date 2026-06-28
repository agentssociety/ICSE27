from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.patient_queue.patient_queue_repo_impl import SQLAlchemyPatientQueueRepository

"""
Api layer for the Dashboard domain class

Package: api.dashboard
Layer: api
Related tasks: #6
Requirement coverage:
- Real-time Patient Dashboard
"""

router = APIRouter()


@router.get("/queue/{queue_id}/overview")
def get_queue_overview(queue_id: int, db: Session = Depends(get_db)):
    """Get dashboard overview for a patient queue."""
    repo = SQLAlchemyPatientQueueRepository(db)
    queue_response = repo.get_by_id(queue_id)
    if queue_response is None:
        # Return empty overview instead of 404 — fresh database has no queue yet
        return {"queue_id": queue_id, "message": "No queue data yet", "status": "empty"}
    return {"queue_id": queue_id, "message": "Dashboard overview endpoint", "status": "ok"}


@router.get("/queue/{queue_id}/patients")
def get_queue_patients(queue_id: int, db: Session = Depends(get_db)):
    """Get all patients in a queue for dashboard display."""
    repo = SQLAlchemyPatientQueueRepository(db)
    queue_response = repo.get_by_id(queue_id)
    if queue_response is None:
        # Return empty list instead of 404 — fresh database has no queue yet
        return {"queue_id": queue_id, "patients": []}

    # Get patients in this queue
    from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository
    patient_repo = SQLAlchemyPatientRepository(db)
    all_patients = patient_repo.get_all()

    # Filter to patients in this queue
    queue_patients = [p for p in all_patients if p.patientQueue_id == queue_id]
    return {"queue_id": queue_id, "patients": [p.model_dump() for p in queue_patients]}
