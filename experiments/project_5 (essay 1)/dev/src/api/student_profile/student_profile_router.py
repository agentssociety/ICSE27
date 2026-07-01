from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.student_profile.student_profile_dto import StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
from src.infra.student_profile.student_profile_repo_impl import SQLAlchemyStudentProfileRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStudentProfileRepository:
    return SQLAlchemyStudentProfileRepository(db)


@router.get("", response_model=list[StudentProfileResponse])
def list_profiles(skip: int = 0, limit: int = 100, student_id: Optional[int] = None,
                  repo: SQLAlchemyStudentProfileRepository = Depends(_repo)):
    if student_id is not None:
        item = repo.get_by_student_id(student_id)
        return [item] if item else []
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StudentProfileResponse)
def get_profile(item_id: int, repo: SQLAlchemyStudentProfileRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentProfile not found")
    return item


@router.post("", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(data: StudentProfileCreate, repo: SQLAlchemyStudentProfileRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StudentProfileResponse)
def update_profile(item_id: int, data: StudentProfileUpdate, repo: SQLAlchemyStudentProfileRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentProfile not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(item_id: int, repo: SQLAlchemyStudentProfileRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentProfile not found")
