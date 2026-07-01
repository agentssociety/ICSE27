from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.enrollment.enrollment_dto import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from src.infra.enrollment.enrollment_repo_impl import SQLAlchemyEnrollmentRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyEnrollmentRepository:
    return SQLAlchemyEnrollmentRepository(db)


@router.get("", response_model=list[EnrollmentResponse])
def list_enrollments(skip: int = 0, limit: int = 100, repo: SQLAlchemyEnrollmentRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=EnrollmentResponse)
def get_enrollment(item_id: int, repo: SQLAlchemyEnrollmentRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return item


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, repo: SQLAlchemyEnrollmentRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=EnrollmentResponse)
def update_enrollment(item_id: int, data: EnrollmentUpdate, repo: SQLAlchemyEnrollmentRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(item_id: int, repo: SQLAlchemyEnrollmentRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
