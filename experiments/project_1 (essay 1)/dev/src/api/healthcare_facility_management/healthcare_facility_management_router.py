from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.healthcare_facility_management.healthcare_facility_management_dto import HealthcareFacilityManagementCreate, HealthcareFacilityManagementUpdate, HealthcareFacilityManagementResponse
from src.infra.healthcare_facility_management.healthcare_facility_management_repo_impl import SQLAlchemyHealthcareFacilityManagementRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyHealthcareFacilityManagementRepository:
    return SQLAlchemyHealthcareFacilityManagementRepository(db)


@router.get("", response_model=list[HealthcareFacilityManagementResponse])
def list_healthcare_facility_managements(skip: int = 0, limit: int = 100, repo: SQLAlchemyHealthcareFacilityManagementRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=HealthcareFacilityManagementResponse)
def get_healthcare_facility_management(item_id: int, repo: SQLAlchemyHealthcareFacilityManagementRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HealthcareFacilityManagement not found")
    return item


@router.post("", response_model=HealthcareFacilityManagementResponse, status_code=status.HTTP_201_CREATED)
def create_healthcare_facility_management(data: HealthcareFacilityManagementCreate, repo: SQLAlchemyHealthcareFacilityManagementRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=HealthcareFacilityManagementResponse)
def update_healthcare_facility_management(item_id: int, data: HealthcareFacilityManagementUpdate, repo: SQLAlchemyHealthcareFacilityManagementRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HealthcareFacilityManagement not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_healthcare_facility_management(item_id: int, repo: SQLAlchemyHealthcareFacilityManagementRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HealthcareFacilityManagement not found")
