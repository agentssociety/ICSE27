from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.suspicious_pattern.suspicious_pattern_dto import SuspiciousPatternCreate, SuspiciousPatternUpdate, SuspiciousPatternResponse
from src.infra.suspicious_pattern.suspicious_pattern_repo_impl import SQLAlchemySuspiciousPatternRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySuspiciousPatternRepository:
    return SQLAlchemySuspiciousPatternRepository(db)


@router.get("", response_model=list[SuspiciousPatternResponse])
def list_suspicious_patterns(skip: int = 0, limit: int = 100, repo: SQLAlchemySuspiciousPatternRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=SuspiciousPatternResponse)
def get_suspicious_pattern(item_id: int, repo: SQLAlchemySuspiciousPatternRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SuspiciousPattern not found")
    return item


@router.post("", response_model=SuspiciousPatternResponse, status_code=status.HTTP_201_CREATED)
def create_suspicious_pattern(data: SuspiciousPatternCreate, repo: SQLAlchemySuspiciousPatternRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=SuspiciousPatternResponse)
def update_suspicious_pattern(item_id: int, data: SuspiciousPatternUpdate, repo: SQLAlchemySuspiciousPatternRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SuspiciousPattern not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_suspicious_pattern(item_id: int, repo: SQLAlchemySuspiciousPatternRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SuspiciousPattern not found")
