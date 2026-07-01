from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.question.question_dto import QuestionCreate, QuestionUpdate, QuestionResponse
from src.infra.question.question_repo_impl import SQLAlchemyQuestionRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyQuestionRepository:
    return SQLAlchemyQuestionRepository(db)


@router.get("", response_model=list[QuestionResponse])
def list_questions(skip: int = 0, limit: int = 100, exam_id: Optional[int] = None, repo: SQLAlchemyQuestionRepository = Depends(_repo)):
    items = repo.get_all(skip=skip, limit=limit)
    if exam_id is not None:
        items = [q for q in items if q.exam_id == exam_id]
    return items


@router.get("/{item_id}", response_model=QuestionResponse)
def get_question(item_id: int, repo: SQLAlchemyQuestionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return item


@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(data: QuestionCreate, repo: SQLAlchemyQuestionRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=QuestionResponse)
def update_question(item_id: int, data: QuestionUpdate, repo: SQLAlchemyQuestionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(item_id: int, repo: SQLAlchemyQuestionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
