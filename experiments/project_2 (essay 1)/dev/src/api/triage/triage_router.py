from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.triage.triage_dto import (
    MessageResponse,
    TriageAssessmentCreate,
    TriageAssessmentResponse,
    TriageQueueEntry,
)
from src.infra.triage.triage_repo_impl import SQLAlchemyTriageRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTriageRepository:
    return SQLAlchemyTriageRepository(db)


@router.post("/assess", response_model=TriageAssessmentResponse, status_code=status.HTTP_201_CREATED)
def assess_patient(data: TriageAssessmentCreate, repo: SQLAlchemyTriageRepository = Depends(_repo)):
    return repo.assess(data)


@router.get("/queue", response_model=list[TriageQueueEntry])
def get_queue(repo: SQLAlchemyTriageRepository = Depends(_repo)):
    return repo.get_queue()


@router.delete("/queue/{patient_id}", response_model=MessageResponse)
def remove_from_queue(patient_id: str, repo: SQLAlchemyTriageRepository = Depends(_repo)):
    if not repo.remove_from_queue(patient_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found in queue",
        )
    return {"message": "Patient removed from queue"}
