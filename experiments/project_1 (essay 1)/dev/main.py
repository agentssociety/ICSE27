from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.database import create_tables
from src.config.settings import settings
from src.api.healthcare_facility_management.healthcare_facility_management_router import router as healthcare_facility_management_router
from src.api.medical_staff.medical_staff_router import router as medical_staff_router
from src.api.patient.patient_router import router as patient_router
from src.api.patient_care_team.patient_care_team_router import router as patient_care_team_router
from src.api.patient_queue.patient_queue_router import router as patient_queue_router
from src.api.patient_record.patient_record_router import router as patient_record_router
from src.api.symptom_resource.symptom_resource_router import router as symptom_resource_router
from src.api.triage_nurse.triage_nurse_router import router as triage_nurse_router
from src.api.urgency_level.urgency_level_router import router as urgency_level_router
from src.api.dashboard.dashboard_router import router as dashboard_router

_log = logging.getLogger(__name__)


def _seed_default_queue() -> None:
    """Create the default PatientQueue (id=1) if it doesn't exist yet."""
    import uuid
    from src.config.database import SessionLocal
    from src.orm.patient_queue.patient_queue_orm import PatientQueueORM
    db = SessionLocal()
    try:
        if not db.get(PatientQueueORM, 1):
            db.add(PatientQueueORM(queueId=uuid.uuid4()))
            db.commit()
            _log.info("Seeded default PatientQueue (id=1).")
    except Exception as exc:
        _log.warning("Could not seed default queue: %s", exc)
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        _log.info("Database tables created / verified.")
        _seed_default_queue()
    except Exception as exc:
        _log.warning("DB unavailable at startup (will retry per request): %s", exc)
    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Auto-generated API",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcare_facility_management_router, prefix="/healthcare_facility_managements", tags=["HealthcareFacilityManagement"])
app.include_router(medical_staff_router, prefix="/medical_staffs", tags=["MedicalStaff"])
app.include_router(patient_router, prefix="/patients", tags=["Patient"])
app.include_router(patient_care_team_router, prefix="/patient_care_teams", tags=["PatientCareTeam"])
app.include_router(patient_queue_router, prefix="/patient_queues", tags=["PatientQueue"])
app.include_router(patient_record_router, prefix="/patient_records", tags=["PatientRecord"])
app.include_router(symptom_resource_router, prefix="/symptom_resources", tags=["SymptomResource"])
app.include_router(triage_nurse_router, prefix="/triage_nurses", tags=["TriageNurse"])
app.include_router(urgency_level_router, prefix="/urgency_levels", tags=["UrgencyLevel"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
