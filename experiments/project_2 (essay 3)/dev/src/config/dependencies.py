from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.blood_type.blood_type_repo_impl import SQLAlchemyBloodTypeRepository
from src.infra.blood_unit.blood_unit_repo_impl import SQLAlchemyBloodUnitRepository
from src.infra.patient_detail.patient_detail_repo_impl import SQLAlchemyPatientDetailRepository
from src.infra.reservation.reservation_repo_impl import SQLAlchemyReservationRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
from src.infra.transfusion_request.transfusion_request_repo_impl import SQLAlchemyTransfusionRequestRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_blood_type_repository(db: Session = Depends(get_db)) -> SQLAlchemyBloodTypeRepository:
    return SQLAlchemyBloodTypeRepository(db)

def get_blood_unit_repository(db: Session = Depends(get_db)) -> SQLAlchemyBloodUnitRepository:
    return SQLAlchemyBloodUnitRepository(db)

def get_patient_detail_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientDetailRepository:
    return SQLAlchemyPatientDetailRepository(db)

def get_reservation_repository(db: Session = Depends(get_db)) -> SQLAlchemyReservationRepository:
    return SQLAlchemyReservationRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)

def get_transfusion_request_repository(db: Session = Depends(get_db)) -> SQLAlchemyTransfusionRequestRepository:
    return SQLAlchemyTransfusionRequestRepository(db)
