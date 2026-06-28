from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.flight.flight_repo_impl import SQLAlchemyFlightRepository
from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_flight_repository(db: Session = Depends(get_db)) -> SQLAlchemyFlightRepository:
    return SQLAlchemyFlightRepository(db)

def get_interface_repository(db: Session = Depends(get_db)) -> SQLAlchemyInterfaceRepository:
    return SQLAlchemyInterfaceRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)

def get_runway_repository(db: Session = Depends(get_db)) -> SQLAlchemyRunwayRepository:
    return SQLAlchemyRunwayRepository(db)
