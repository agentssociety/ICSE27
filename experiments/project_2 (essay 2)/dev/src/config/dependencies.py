from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.blood_unit.blood_unit_repo_impl import SQLAlchemyBloodUnitRepository
from src.infra.reservation.reservation_repo_impl import SQLAlchemyReservationRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_blood_unit_repository(db: Session = Depends(get_db)) -> SQLAlchemyBloodUnitRepository:
    return SQLAlchemyBloodUnitRepository(db)

def get_reservation_repository(db: Session = Depends(get_db)) -> SQLAlchemyReservationRepository:
    return SQLAlchemyReservationRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)
