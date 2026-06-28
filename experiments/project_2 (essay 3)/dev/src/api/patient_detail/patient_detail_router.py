from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.patient_detail.patient_detail_dto import PatientDetailCreate, PatientDetailUpdate, PatientDetailResponse
from src.infra.patient_detail.patient_detail_repo_impl import SQLAlchemyPatientDetailRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPatientDetailRepository:
    return SQLAlchemyPatientDetailRepository(db)


@router.get("", response_model=list[PatientDetailResponse])
def list_patient_details(skip: int = 0, limit: int = 100, repo: SQLAlchemyPatientDetailRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=PatientDetailResponse)
def get_patient_detail(item_id: int, repo: SQLAlchemyPatientDetailRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientDetail not found")
    return item


@router.post("", response_model=PatientDetailResponse, status_code=status.HTTP_201_CREATED)
def create_patient_detail(data: PatientDetailCreate, repo: SQLAlchemyPatientDetailRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=PatientDetailResponse)
def update_patient_detail(item_id: int, data: PatientDetailUpdate, repo: SQLAlchemyPatientDetailRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientDetail not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_detail(item_id: int, repo: SQLAlchemyPatientDetailRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PatientDetail not found")
