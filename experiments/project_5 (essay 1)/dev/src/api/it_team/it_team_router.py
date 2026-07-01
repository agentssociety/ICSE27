from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.it_team.it_team_dto import IT_TeamCreate, IT_TeamUpdate, IT_TeamResponse
from src.infra.it_team.it_team_repo_impl import SQLAlchemyIT_TeamRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyIT_TeamRepository:
    return SQLAlchemyIT_TeamRepository(db)


@router.get("", response_model=list[IT_TeamResponse])
def list_it_teams(skip: int = 0, limit: int = 100, repo: SQLAlchemyIT_TeamRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=IT_TeamResponse)
def get_it_team(item_id: int, repo: SQLAlchemyIT_TeamRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IT_Team not found")
    return item


@router.post("", response_model=IT_TeamResponse, status_code=status.HTTP_201_CREATED)
def create_it_team(data: IT_TeamCreate, repo: SQLAlchemyIT_TeamRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=IT_TeamResponse)
def update_it_team(item_id: int, data: IT_TeamUpdate, repo: SQLAlchemyIT_TeamRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IT_Team not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_it_team(item_id: int, repo: SQLAlchemyIT_TeamRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IT_Team not found")
