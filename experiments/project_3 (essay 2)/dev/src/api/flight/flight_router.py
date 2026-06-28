from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.flight.flight_dto import FlightRegistrationRequest, FlightUpdateRequest, FlightResponse
from src.infra.flight.flight_repo_impl import SQLAlchemyFlightRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyFlightRepository:
    return SQLAlchemyFlightRepository(db)


@router.get("", response_model=list[FlightResponse])
def list_flights(skip: int = 0, limit: int = 100, repo: SQLAlchemyFlightRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=FlightResponse)
def get_flight(item_id: int, repo: SQLAlchemyFlightRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return item


@router.post("", response_model=FlightResponse, status_code=status.HTTP_201_CREATED)
def create_flight(data: FlightRegistrationRequest, repo: SQLAlchemyFlightRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=FlightResponse)
def update_flight(item_id: int, data: FlightUpdateRequest, repo: SQLAlchemyFlightRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(item_id: int, repo: SQLAlchemyFlightRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")