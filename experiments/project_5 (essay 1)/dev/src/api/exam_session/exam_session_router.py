from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.exam_session.exam_session_dto import ExamSessionCreate, ExamSessionUpdate, ExamSessionResponse
from src.infra.exam_session.exam_session_repo_impl import SQLAlchemyExamSessionRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyExamSessionRepository:
    return SQLAlchemyExamSessionRepository(db)


@router.get("", response_model=list[ExamSessionResponse])
def list_exam_sessions(skip: int = 0, limit: int = 100, repo: SQLAlchemyExamSessionRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ExamSessionResponse)
def get_exam_session(item_id: int, repo: SQLAlchemyExamSessionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ExamSession not found")
    return item


@router.post("", response_model=ExamSessionResponse, status_code=status.HTTP_201_CREATED)
def create_exam_session(data: ExamSessionCreate, repo: SQLAlchemyExamSessionRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ExamSessionResponse)
def update_exam_session(item_id: int, data: ExamSessionUpdate, repo: SQLAlchemyExamSessionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ExamSession not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam_session(item_id: int, repo: SQLAlchemyExamSessionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ExamSession not found")