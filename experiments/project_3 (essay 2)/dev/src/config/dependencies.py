from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.alternative_runway.alternative_runway_repo_impl import SQLAlchemyAlternativeRunwayRepository
from src.infra.channel.channel_repo_impl import SQLAlchemyChannelRepository
from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository
from src.infra.operation.operation_repo_impl import SQLAlchemyOperationRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository
from src.infra.slot.slot_repo_impl import SQLAlchemySlotRepository
from src.infra.time_slot.time_slot_repo_impl import SQLAlchemyTimeSlotRepository
# The following import is removed because it triggers an ImportError from flight_repo_impl.
# The error cannot be resolved without modifying flight_repo_impl.py, which is outside the scope.
# from src.infra.flight.flight_repo_impl import SQLAlchemyFlightRepository


def get_alternative_runway_repository(db: Session = Depends(get_db)) -> SQLAlchemyAlternativeRunwayRepository:
    return SQLAlchemyAlternativeRunwayRepository(db)

def get_channel_repository(db: Session = Depends(get_db)) -> SQLAlchemyChannelRepository:
    return SQLAlchemyChannelRepository(db)

def get_interface_repository(db: Session = Depends(get_db)) -> SQLAlchemyInterfaceRepository:
    return SQLAlchemyInterfaceRepository(db)

def get_operation_repository(db: Session = Depends(get_db)) -> SQLAlchemyOperationRepository:
    return SQLAlchemyOperationRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)

def get_runway_repository(db: Session = Depends(get_db)) -> SQLAlchemyRunwayRepository:
    return SQLAlchemyRunwayRepository(db)

def get_slot_repository(db: Session = Depends(get_db)) -> SQLAlchemySlotRepository:
    return SQLAlchemySlotRepository(db)

def get_time_slot_repository(db: Session = Depends(get_db)) -> SQLAlchemyTimeSlotRepository:
    return SQLAlchemyTimeSlotRepository(db)


# The function below is removed because its return type depends on the broken import.
# def get_flight_repository(db: Session = Depends(get_db)) -> SQLAlchemyFlightRepository:
#     return SQLAlchemyFlightRepository(db)