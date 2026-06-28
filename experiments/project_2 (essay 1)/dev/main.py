from __future__ import annotations

import sys
import os
from contextlib import asynccontextmanager

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi import FastAPI
except ImportError:
    print("FastAPI is not installed. Install it with: pip install fastapi")
    sys.exit(1)

try:
    import uvicorn
except ImportError:
    print("uvicorn is not installed. Install it with: pip install uvicorn")
    sys.exit(1)

try:
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    print("fastapi.middleware.cors is not available. Install FastAPI with: pip install fastapi")
    sys.exit(1)

# Import routers
try:
    from src.api.blood_unit.blood_unit_router import router as blood_unit_router
except ImportError:
    print("Failed to import blood_unit_router. Ensure src/api/blood_unit/blood_unit_router.py exists and has a 'router' object.")
    sys.exit(1)

try:
    from src.api.transfusion_request.transfusion_request_router import router as transfusion_request_router
except ImportError:
    print("Failed to import transfusion_request_router. Ensure src/api/transfusion_request/transfusion_request_router.py exists and has a 'router' object.")
    sys.exit(1)

try:
    from src.api.reservation.reservation_router import router as reservation_router
except ImportError:
    print("Failed to import reservation_router. Ensure src/api/reservation/reservation_router.py exists and has a 'router' object.")
    sys.exit(1)

try:
    from src.api.blood_type_alert_operation.blood_type_alert_operation_router import router as blood_type_alert_operation_router
except ImportError:
    print("Failed to import blood_type_alert_operation_router. Ensure src/api/blood_type_alert_operation/blood_type_alert_operation_router.py exists and has a 'router' object.")
    sys.exit(1)

try:
    from src.api.user.user_router import router as user_router
except ImportError:
    print("Failed to import user_router. Ensure src/api/user/user_router.py exists and has a 'router' object.")
    sys.exit(1)

try:
    from src.api.patient.patient_router import router as patient_router
except ImportError:
    print("Failed to import patient_router.")
    sys.exit(1)

try:
    from src.api.triage.triage_router import router as triage_router
except ImportError:
    print("Failed to import triage_router.")
    sys.exit(1)

try:
    from src.api.dashboard.dashboard_router import router as dashboard_router
except ImportError:
    print("Failed to import dashboard_router.")
    sys.exit(1)

# Note: src/api/alert/alert_router is NOT a FastAPI router — it only contains
# adapter classes (InventoryApiAdapter, NotificationGatewayAdapter) and has
# no `router = APIRouter()` object.  No endpoint router exists for the alert
# domain in the generated scaffold.


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    from src.config.database import engine
    from src.orm.base import Base
    # Import new ORM models so their tables are registered on Base.metadata
    from src.orm.patient.patient_orm import PatientORM  # noqa: F401
    from src.orm.triage.triage_orm import TriageAssessmentORM  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Also create tables for the pre-existing ORM models that use their own Base classes
    from src.orm.blood_unit.blood_unit_orm import Base as BloodUnitBase
    from src.orm.blood_unit.blood_unit_orm import BloodUnitORM  # noqa: F401
    BloodUnitBase.metadata.create_all(bind=engine)

    from src.orm.transfusion_request.transfusion_request_orm import Base as TransfusionBase
    from src.orm.transfusion_request.transfusion_request_orm import TransfusionRequestORM  # noqa: F401
    TransfusionBase.metadata.create_all(bind=engine)

    from src.orm.reservation.reservation_orm import Base as ReservationBase
    from src.orm.reservation.reservation_orm import ReservationORM  # noqa: F401
    ReservationBase.metadata.create_all(bind=engine)

    from src.orm.blood_type_alert_operation.blood_type_alert_operation_orm import Base as BTAOBase
    from src.orm.blood_type_alert_operation.blood_type_alert_operation_orm import BloodTypeAlertOperationORM  # noqa: F401
    BTAOBase.metadata.create_all(bind=engine)

    from src.orm.user.user_orm import Base as UserBase
    from src.orm.user.user_orm import UserORM  # noqa: F401
    UserBase.metadata.create_all(bind=engine)

    yield


# Create FastAPI app
app = FastAPI(
    title="Blood Bank & Triage Manager",
    description="REST API for managing blood bank inventory, transfusion requests, reservations, alerts, patients, and triage queue.",
    version="1.0.0",
    redirect_slashes=False,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(blood_unit_router, prefix="/api/blood-units", tags=["Blood Units"])
app.include_router(transfusion_request_router, prefix="/api/transfusion-requests", tags=["Transfusion Requests"])
app.include_router(reservation_router, prefix="/api/reservations", tags=["Reservations"])
app.include_router(blood_type_alert_operation_router, prefix="/api/blood-type-alert-operations", tags=["Blood Type Alert Operations"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(triage_router, prefix="/api/triage", tags=["Triage"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,  # Changed from 8000 to avoid "Address already in use" error
        reload=True,
    )
