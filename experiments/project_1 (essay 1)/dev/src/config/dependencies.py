from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.healthcare_facility_management.healthcare_facility_management_repo_impl import SQLAlchemyHealthcareFacilityManagementRepository
from src.infra.medical_staff.medical_staff_repo_impl import SQLAlchemyMedicalStaffRepository
from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository
from src.infra.patient_care_team.patient_care_team_repo_impl import SQLAlchemyPatientCareTeamRepository
from src.infra.patient_queue.patient_queue_repo_impl import SQLAlchemyPatientQueueRepository
from src.infra.patient_record.patient_record_repo_impl import SQLAlchemyPatientRecordRepository
from src.infra.symptom_resource.symptom_resource_repo_impl import SQLAlchemySymptomResourceRepository
from src.infra.triage_nurse.triage_nurse_repo_impl import SQLAlchemyTriageNurseRepository


def get_healthcare_facility_management_repository(db: Session = Depends(get_db)) -> SQLAlchemyHealthcareFacilityManagementRepository:
    return SQLAlchemyHealthcareFacilityManagementRepository(db)

def get_medical_staff_repository(db: Session = Depends(get_db)) -> SQLAlchemyMedicalStaffRepository:
    return SQLAlchemyMedicalStaffRepository(db)

def get_patient_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientRepository:
    return SQLAlchemyPatientRepository(db)

def get_patient_care_team_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientCareTeamRepository:
    return SQLAlchemyPatientCareTeamRepository(db)

def get_patient_queue_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientQueueRepository:
    return SQLAlchemyPatientQueueRepository(db)

def get_patient_record_repository(db: Session = Depends(get_db)) -> SQLAlchemyPatientRecordRepository:
    return SQLAlchemyPatientRecordRepository(db)

def get_symptom_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemySymptomResourceRepository:
    return SQLAlchemySymptomResourceRepository(db)

def get_triage_nurse_repository(db: Session = Depends(get_db)) -> SQLAlchemyTriageNurseRepository:
    return SQLAlchemyTriageNurseRepository(db)
