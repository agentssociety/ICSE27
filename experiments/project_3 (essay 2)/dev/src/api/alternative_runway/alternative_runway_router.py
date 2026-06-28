from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.alternative_runway.alternative_runway_dto import AlternativeRunwayCreate, AlternativeRunwayUpdate, AlternativeRunwayResponse
from src.infra.alternative_runway.alternative_runway_repo_impl import SQLAlchemyAlternativeRunwayRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAlternativeRunwayRepository:
    return SQLAlchemyAlternativeRunwayRepository(db)


@router.get("", response_model=list[AlternativeRunwayResponse])
def list_alternative_runways(skip: int = 0, limit: int = 100, repo: SQLAlchemyAlternativeRunwayRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AlternativeRunwayResponse)
def get_alternative_runway(item_id: int, repo: SQLAlchemyAlternativeRunwayRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AlternativeRunway not found")
    return item


@router.post("", response_model=AlternativeRunwayResponse, status_code=status.HTTP_201_CREATED)
def create_alternative_runway(data: AlternativeRunwayCreate, repo: SQLAlchemyAlternativeRunwayRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AlternativeRunwayResponse)
def update_alternative_runway(item_id: int, data: AlternativeRunwayUpdate, repo: SQLAlchemyAlternativeRunwayRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AlternativeRunway not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alternative_runway(item_id: int, repo: SQLAlchemyAlternativeRunwayRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AlternativeRunway not found")
