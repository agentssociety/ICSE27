from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.aircraft.aircraft_dto import AircraftCreate, AircraftUpdate, AircraftResponse
from src.infra.aircraft.aircraft_repo_impl import SQLAlchemyAircraftRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAircraftRepository:
    return SQLAlchemyAircraftRepository(db)


@router.get("", response_model=list[AircraftResponse])
def list_aircrafts(skip: int = 0, limit: int = 100, repo: SQLAlchemyAircraftRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AircraftResponse)
def get_aircraft(item_id: int, repo: SQLAlchemyAircraftRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aircraft not found")
    return item


@router.post("", response_model=AircraftResponse, status_code=status.HTTP_201_CREATED)
def create_aircraft(data: AircraftCreate, repo: SQLAlchemyAircraftRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AircraftResponse)
def update_aircraft(item_id: int, data: AircraftUpdate, repo: SQLAlchemyAircraftRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aircraft not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aircraft(item_id: int, repo: SQLAlchemyAircraftRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aircraft not found")
