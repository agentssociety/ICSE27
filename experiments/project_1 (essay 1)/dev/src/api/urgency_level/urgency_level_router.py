from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.urgency_level.urgency_level_dto import UrgencyLevelCreateRequest, UrgencyLevelUpdateRequest, UrgencyLevelResponse
from src.infra.urgency_level.urgency_level_repo_impl import SQLAlchemyUrgencyLevelRepository

"""
Api layer for the UrgencyLevel domain class

Package: api.urgency_level
Layer: api
Related tasks: #2, #3, #4, #6
Requirement coverage:
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Real-time Patient Dashboard
"""

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyUrgencyLevelRepository:
    return SQLAlchemyUrgencyLevelRepository(db)


@router.get("", response_model=list[UrgencyLevelResponse])
def list_urgency_levels(skip: int = 0, limit: int = 100, repo: SQLAlchemyUrgencyLevelRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=UrgencyLevelResponse)
def get_urgency_level(item_id: int, repo: SQLAlchemyUrgencyLevelRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UrgencyLevel not found")
    return item


@router.post("", response_model=UrgencyLevelResponse, status_code=status.HTTP_201_CREATED)
def create_urgency_level(data: UrgencyLevelCreateRequest, repo: SQLAlchemyUrgencyLevelRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=UrgencyLevelResponse)
def update_urgency_level(item_id: int, data: UrgencyLevelUpdateRequest, repo: SQLAlchemyUrgencyLevelRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UrgencyLevel not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_urgency_level(item_id: int, repo: SQLAlchemyUrgencyLevelRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UrgencyLevel not found")
