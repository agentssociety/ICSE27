from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.database import create_tables
from src.config.settings import settings
from src.api.actor.actor_router import router as actor_router
from src.api.interface.interface_router import router as interface_router
try:
    from src.api.patient.patient_router import router as patient_router
except ImportError:
    patient_router = APIRouter()
from src.api.resource.resource_router import router as resource_router
from src.api.symptom.symptom_router import router as symptom_router
from src.api.symptom_record.symptom_record_router import router as symptom_record_router
from src.api.user_authentication_system.user_authentication_system_router import router as user_authentication_system_router

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        _log.info("Database tables created / verified.")
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

app.include_router(actor_router, prefix="/actors", tags=["Actor"])
app.include_router(interface_router, prefix="/interfaces", tags=["Interface"])
app.include_router(patient_router, prefix="/patients", tags=["Patient"])
app.include_router(resource_router, prefix="/resources", tags=["Resource"])
app.include_router(symptom_router, prefix="/symptoms", tags=["Symptom"])
app.include_router(symptom_record_router, prefix="/symptom_records", tags=["SymptomRecord"])
app.include_router(user_authentication_system_router, prefix="/user_authentication_systems", tags=["UserAuthenticationSystem"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")