from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.competency.competency_dto import CompetencyCreate, CompetencyUpdate, CompetencyResponse
from src.infra.competency.competency_repo_impl import SQLAlchemyCompetencyRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCompetencyRepository:
    return SQLAlchemyCompetencyRepository(db)


@router.get("", response_model=list[CompetencyResponse])
def list_competencys(skip: int = 0, limit: int = 100, repo: SQLAlchemyCompetencyRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CompetencyResponse)
def get_competency(item_id: int, repo: SQLAlchemyCompetencyRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found")
    return item


@router.post("", response_model=CompetencyResponse, status_code=status.HTTP_201_CREATED)
def create_competency(data: CompetencyCreate, repo: SQLAlchemyCompetencyRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CompetencyResponse)
def update_competency(item_id: int, data: CompetencyUpdate, repo: SQLAlchemyCompetencyRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competency(item_id: int, repo: SQLAlchemyCompetencyRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competency not found")
