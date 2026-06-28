from __future__ import annotations



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.reservation.reservation_dto import ReservationCreate, ReservationUpdate, ReservationResponse
from src.infra.reservation.reservation_repo_impl import SQLAlchemyReservationRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyReservationRepository:
    return SQLAlchemyReservationRepository(db)


@router.get("", response_model=list[ReservationResponse])
def list_reservations(skip: int = 0, limit: int = 100, repo: SQLAlchemyReservationRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ReservationResponse)
def get_reservation(item_id: int, repo: SQLAlchemyReservationRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return item


@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(data: ReservationCreate, repo: SQLAlchemyReservationRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ReservationResponse)
def update_reservation(item_id: int, data: ReservationUpdate, repo: SQLAlchemyReservationRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(item_id: int, repo: SQLAlchemyReservationRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
