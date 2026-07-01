from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.cohort.cohort_dto import CohortCreate, CohortUpdate, CohortResponse
from src.infra.cohort.cohort_repo_impl import SQLAlchemyCohortRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCohortRepository:
    return SQLAlchemyCohortRepository(db)


@router.get("", response_model=list[CohortResponse])
def list_cohorts(skip: int = 0, limit: int = 100, repo: SQLAlchemyCohortRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CohortResponse)
def get_cohort(item_id: int, repo: SQLAlchemyCohortRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cohort not found")
    return item


@router.post("", response_model=CohortResponse, status_code=status.HTTP_201_CREATED)
def create_cohort(data: CohortCreate, repo: SQLAlchemyCohortRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CohortResponse)
def update_cohort(item_id: int, data: CohortUpdate, repo: SQLAlchemyCohortRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cohort not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cohort(item_id: int, repo: SQLAlchemyCohortRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cohort not found")
