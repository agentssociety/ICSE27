from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.medical_staff.medical_staff_dto import MedicalStaffCreate, MedicalStaffUpdate, MedicalStaffResponse
from src.infra.medical_staff.medical_staff_repo_impl import SQLAlchemyMedicalStaffRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyMedicalStaffRepository:
    return SQLAlchemyMedicalStaffRepository(db)


@router.get("", response_model=list[MedicalStaffResponse])
def list_medical_staffs(skip: int = 0, limit: int = 100, repo: SQLAlchemyMedicalStaffRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=MedicalStaffResponse)
def get_medical_staff(item_id: int, repo: SQLAlchemyMedicalStaffRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalStaff not found")
    return item


@router.post("", response_model=MedicalStaffResponse, status_code=status.HTTP_201_CREATED)
def create_medical_staff(data: MedicalStaffCreate, repo: SQLAlchemyMedicalStaffRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=MedicalStaffResponse)
def update_medical_staff(item_id: int, data: MedicalStaffUpdate, repo: SQLAlchemyMedicalStaffRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalStaff not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_staff(item_id: int, repo: SQLAlchemyMedicalStaffRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalStaff not found")
