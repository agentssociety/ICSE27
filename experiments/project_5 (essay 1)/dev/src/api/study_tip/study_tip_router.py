from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.study_tip.study_tip_dto import StudyTipCreate, StudyTipUpdate, StudyTipResponse
from src.infra.study_tip.study_tip_repo_impl import SQLAlchemyStudyTipRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStudyTipRepository:
    return SQLAlchemyStudyTipRepository(db)


@router.get("", response_model=list[StudyTipResponse])
def list_tips(skip: int = 0, limit: int = 100, competency_name: Optional[str] = None,
              repo: SQLAlchemyStudyTipRepository = Depends(_repo)):
    if competency_name is not None:
        return repo.get_by_competency(competency_name)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StudyTipResponse)
def get_tip(item_id: int, repo: SQLAlchemyStudyTipRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudyTip not found")
    return item


@router.post("", response_model=StudyTipResponse, status_code=status.HTTP_201_CREATED)
def create_tip(data: StudyTipCreate, repo: SQLAlchemyStudyTipRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StudyTipResponse)
def update_tip(item_id: int, data: StudyTipUpdate, repo: SQLAlchemyStudyTipRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudyTip not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tip(item_id: int, repo: SQLAlchemyStudyTipRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudyTip not found")
