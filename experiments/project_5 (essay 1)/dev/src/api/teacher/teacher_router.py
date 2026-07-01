from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.teacher.teacher_dto import TeacherCreate, TeacherUpdate, TeacherResponse
from src.infra.teacher.teacher_repo_impl import SQLAlchemyTeacherRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTeacherRepository:
    return SQLAlchemyTeacherRepository(db)


@router.get("", response_model=list[TeacherResponse])
def list_teachers(skip: int = 0, limit: int = 100, repo: SQLAlchemyTeacherRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TeacherResponse)
def get_teacher(item_id: int, repo: SQLAlchemyTeacherRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return item


@router.post("", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(data: TeacherCreate, repo: SQLAlchemyTeacherRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TeacherResponse)
def update_teacher(item_id: int, data: TeacherUpdate, repo: SQLAlchemyTeacherRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(item_id: int, repo: SQLAlchemyTeacherRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
