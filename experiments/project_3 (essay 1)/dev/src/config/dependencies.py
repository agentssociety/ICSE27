from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db


def get_actor_repository(db: Session = Depends(get_db)) -> "SQLAlchemyActorRepository":
    from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
    return SQLAlchemyActorRepository(db)


def get_aircraft_repository(db: Session = Depends(get_db)) -> "SQLAlchemyAircraftRepository":
    from src.infra.aircraft.aircraft_repo_impl import SQLAlchemyAircraftRepository
    return SQLAlchemyAircraftRepository(db)


def get_flight_repository(db: Session = Depends(get_db)) -> "SQLAlchemyFlightRepository":
    from src.infra.flight.flight_repo_impl import SQLAlchemyFlightRepository
    return SQLAlchemyFlightRepository(db)


def get_interface_repository(db: Session = Depends(get_db)) -> "SQLAlchemyInterfaceRepository":
    from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository
    return SQLAlchemyInterfaceRepository(db)


def get_operation_repository(db: Session = Depends(get_db)) -> "SQLAlchemyOperationRepository":
    from src.infra.operation.operation_repo_impl import SQLAlchemyOperationRepository
    return SQLAlchemyOperationRepository(db)


def get_operation_slot_repository(db: Session = Depends(get_db)) -> "SQLAlchemyOperationSlotRepository":
    from src.infra.operation_slot.operation_slot_repo_impl import SQLAlchemyOperationSlotRepository
    return SQLAlchemyOperationSlotRepository(db)


def get_permission_repository(db: Session = Depends(get_db)) -> "SQLAlchemyPermissionRepository":
    from src.infra.permission.permission_repo_impl import SQLAlchemyPermissionRepository
    return SQLAlchemyPermissionRepository(db)


def get_resource_repository(db: Session = Depends(get_db)) -> "SQLAlchemyResourceRepository":
    from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
    return SQLAlchemyResourceRepository(db)


def get_runway_repository(db: Session = Depends(get_db)) -> "SQLAlchemyRunwayRepository":
    from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository
    return SQLAlchemyRunwayRepository(db)


def get_separation_rule_repository(db: Session = Depends(get_db)) -> "SQLAlchemySeparationRuleRepository":
    from src.infra.separation_rule.separation_rule_repo_impl import SQLAlchemySeparationRuleRepository
    return SQLAlchemySeparationRuleRepository(db)


def get_slot_repository(db: Session = Depends(get_db)) -> "SQLAlchemySlotRepository":
    from src.infra.slot.slot_repo_impl import SQLAlchemySlotRepository
    return SQLAlchemySlotRepository(db)


def get_state_repository(db: Session = Depends(get_db)) -> "SQLAlchemyStateRepository":
    from src.infra.state.state_repo_impl import SQLAlchemyStateRepository
    return SQLAlchemyStateRepository(db)


def get_traffic_data_repository(db: Session = Depends(get_db)) -> "SQLAlchemyTrafficDataRepository":
    from src.infra.traffic_data.traffic_data_repo_impl import SQLAlchemyTrafficDataRepository
    return SQLAlchemyTrafficDataRepository(db)