from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.student.student_dto import StudentCreate, StudentUpdate, StudentResponse
from src.infra.student.student_repo_impl import SQLAlchemyStudentRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStudentRepository:
    return SQLAlchemyStudentRepository(db)


@router.get("", response_model=list[StudentResponse])
def list_students(skip: int = 0, limit: int = 100, repo: SQLAlchemyStudentRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StudentResponse)
def get_student(item_id: int, repo: SQLAlchemyStudentRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return item


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, repo: SQLAlchemyStudentRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StudentResponse)
def update_student(item_id: int, data: StudentUpdate, repo: SQLAlchemyStudentRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(item_id: int, repo: SQLAlchemyStudentRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
