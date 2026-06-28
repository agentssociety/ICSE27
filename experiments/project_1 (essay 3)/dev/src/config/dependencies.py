from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository
from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
from src.infra.symptom.symptom_repo_impl import SQLAlchemySymptomRepository
from src.infra.symptom_record.symptom_record_repo_impl import SQLAlchemySymptomRecordRepository
from src.infra.user_authentication_system.user_authentication_system_repo_impl import SQLAlchemyUserAuthenticationSystemRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_interface_repository(db: Session = Depends(get_db)) -> SQLAlchemyInterfaceRepository:
    return SQLAlchemyInterfaceRepository(db)

def get_patient_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientRepository:
    return SQLAlchemyPatientRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)

def get_symptom_repository(db: Session = Depends(get_db)) -> SQLAlchemySymptomRepository:
    return SQLAlchemySymptomRepository(db)

def get_symptom_record_repository(db: Session = Depends(get_db)) -> SQLAlchemySymptomRecordRepository:
    return SQLAlchemySymptomRecordRepository(db)

def get_user_authentication_system_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserAuthenticationSystemRepository:
    return SQLAlchemyUserAuthenticationSystemRepository(db)
