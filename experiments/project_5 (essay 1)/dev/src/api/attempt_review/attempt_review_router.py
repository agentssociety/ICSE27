from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.attempt_review.attempt_review_dto import AttemptReviewCreate, AttemptReviewUpdate, AttemptReviewResponse
from src.infra.attempt_review.attempt_review_repo_impl import SQLAlchemyAttemptReviewRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAttemptReviewRepository:
    return SQLAlchemyAttemptReviewRepository(db)


@router.get("", response_model=list[AttemptReviewResponse])
def list_attempt_reviews(skip: int = 0, limit: int = 100, repo: SQLAlchemyAttemptReviewRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AttemptReviewResponse)
def get_attempt_review(item_id: int, repo: SQLAlchemyAttemptReviewRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AttemptReview not found")
    return item


@router.post("", response_model=AttemptReviewResponse, status_code=status.HTTP_201_CREATED)
def create_attempt_review(data: AttemptReviewCreate, repo: SQLAlchemyAttemptReviewRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AttemptReviewResponse)
def update_attempt_review(item_id: int, data: AttemptReviewUpdate, repo: SQLAlchemyAttemptReviewRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AttemptReview not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attempt_review(item_id: int, repo: SQLAlchemyAttemptReviewRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AttemptReview not found")
