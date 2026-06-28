from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse
from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRunwayRepository:
    return SQLAlchemyRunwayRepository(db)


@router.get("", response_model=list[RunwayResponse])
def list_runways(skip: int = 0, limit: int = 100, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RunwayResponse)
def get_runway(item_id: int, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
    return item


@router.post("", response_model=RunwayResponse, status_code=status.HTTP_201_CREATED)
def create_runway(data: RunwayCreate, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RunwayResponse)
def update_runway(item_id: int, data: RunwayUpdate, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_runway(item_id: int, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
