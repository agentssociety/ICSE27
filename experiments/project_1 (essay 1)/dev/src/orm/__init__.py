# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.healthcare_facility_management.healthcare_facility_management_orm import HealthcareFacilityManagementORM  # noqa: F401
from src.orm.medical_staff.medical_staff_orm import MedicalStaffORM  # noqa: F401
from src.orm.patient.patient_orm import PatientORM  # noqa: F401
from src.orm.patient_care_team.patient_care_team_orm import PatientCareTeamORM  # noqa: F401
from src.orm.patient_queue.patient_queue_orm import PatientQueueORM  # noqa: F401
from src.orm.patient_record.patient_record_orm import PatientRecordORM  # noqa: F401
from src.orm.symptom_resource.symptom_resource_orm import SymptomResourceORM  # noqa: F401
from src.orm.triage_nurse.triage_nurse_orm import TriageNurseORM  # noqa: F401
from src.orm.urgency_level.urgency_level_orm import UrgencyLevelORM  # noqa: F401
