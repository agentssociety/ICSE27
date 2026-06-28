from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.triage_nurse.triage_nurse_dto import TriageNurseCreate, TriageNurseUpdate, TriageNurseResponse
from src.infra.triage_nurse.triage_nurse_repo_impl import SQLAlchemyTriageNurseRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTriageNurseRepository:
    return SQLAlchemyTriageNurseRepository(db)


@router.get("", response_model=list[TriageNurseResponse])
def list_triage_nurses(skip: int = 0, limit: int = 100, repo: SQLAlchemyTriageNurseRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TriageNurseResponse)
def get_triage_nurse(item_id: int, repo: SQLAlchemyTriageNurseRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TriageNurse not found")
    return item


@router.post("", response_model=TriageNurseResponse, status_code=status.HTTP_201_CREATED)
def create_triage_nurse(data: TriageNurseCreate, repo: SQLAlchemyTriageNurseRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=TriageNurseResponse)
def update_triage_nurse(item_id: int, data: TriageNurseUpdate, repo: SQLAlchemyTriageNurseRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TriageNurse not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_triage_nurse(item_id: int, repo: SQLAlchemyTriageNurseRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TriageNurse not found")
