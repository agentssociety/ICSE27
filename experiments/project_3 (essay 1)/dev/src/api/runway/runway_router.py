from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse, RunwayTimetableResponse, TimetableEntry
from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository
from src.orm.runway.runway_orm import RunwayORM
from src.orm.slot.slot_orm import SlotORM
from src.orm.flight.flight_orm import FlightORM

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRunwayRepository:
    return SQLAlchemyRunwayRepository(db)


@router.get("", response_model=list[RunwayResponse])
def list_runways(skip: int = 0, limit: int = 100, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.post("", response_model=RunwayResponse, status_code=status.HTTP_201_CREATED)
def create_runway(data: RunwayCreate, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    return repo.create(data)


# IMPORTANT: timetable endpoint must be defined before the catch-all {runway_id} path
@router.get("/{runway_id}/timetable", response_model=RunwayTimetableResponse)
def get_runway_timetable(runway_id: str, db: Session = Depends(get_db)):
    runway_orm = db.query(RunwayORM).filter(RunwayORM.id == runway_id).first()
    if runway_orm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")

    entries: list[TimetableEntry] = []

    # If runway has a slot, include it
    if runway_orm.slot is not None:
        slot: SlotORM = runway_orm.slot
        entries.append(TimetableEntry(
            slot_id=slot.id,
            slot_time=slot.time,
            status="allocated" if slot.isAvailable else "occupied",
        ))

    # Fetch all flights and add as timetable entries
    flights = db.query(FlightORM).all()
    for flight in flights:
        entries.append(TimetableEntry(
            flight_id=flight.id,
            flight_number=flight.flightNumber,
            aircraft_type=flight.aircraftType,
            status="scheduled",
        ))

    return RunwayTimetableResponse(
        runway_id=runway_id,
        runway_status=runway_orm.configuration,
        entries=entries,
    )


@router.get("/{runway_id}", response_model=RunwayResponse)
def get_runway(runway_id: str, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    item = repo.get_by_id(runway_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
    return item


@router.put("/{runway_id}", response_model=RunwayResponse)
def update_runway(runway_id: str, data: RunwayUpdate, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    item = repo.update(runway_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
    return item


@router.delete("/{runway_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_runway(runway_id: str, repo: SQLAlchemyRunwayRepository = Depends(_repo)):
    if not repo.delete(runway_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Runway not found")
