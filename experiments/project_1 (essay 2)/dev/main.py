from __future__ import annotations

from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI
except ImportError:
    print("Install FastAPI: pip install fastapi")
    raise

try:
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    print("Install FastAPI: pip install fastapi")
    raise

try:
    from src.config.database import engine, Base
except ImportError:
    print("Ensure src.config.database exists")
    raise

try:
    from src.api.patient.patient_router import router as patient_router
except ImportError:
    print("Ensure src.api.patient.patient_router exists")
    raise

try:
    from src.api.patient_record.patient_record_router import router as patient_record_router
except ImportError:
    print("Ensure src.api.patient_record.patient_record_router exists")
    raise

try:
    from src.api.queue_entry.queue_entry_router import router as queue_entry_router
except ImportError:
    print("Ensure src.api.queue_entry.queue_entry_router exists")
    raise

# Import all ORM models so they register with Base.metadata
import src.orm.patient.patient_orm  # noqa: F401
import src.orm.patient_record.patient_record_orm  # noqa: F401
import src.orm.queue_entry.queue_entry_orm  # noqa: F401
import src.orm.symptom_data.symptom_data_orm  # noqa: F401
import src.orm.resource.resource_orm  # noqa: F401
import src.orm.data_at_rest_encryption.data_at_rest_encryption_orm  # noqa: F401


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Startup: create all database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing to do


app = FastAPI(redirect_slashes=False, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(patient_record_router, prefix="/api/v1/patient_records", tags=["patient_records"])
app.include_router(queue_entry_router, prefix="/api/v1/queue_entries", tags=["queue_entries"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("Install uvicorn: pip install uvicorn")
        raise
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
