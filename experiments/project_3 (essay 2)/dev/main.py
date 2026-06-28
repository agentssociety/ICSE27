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
from src.api.alternative_runway.alternative_runway_router import router as alternative_runway_router
from src.api.channel.channel_router import router as channel_router
from src.api.interface.interface_router import router as interface_router
from src.api.operation.operation_router import router as operation_router
from src.api.resource.resource_router import router as resource_router
from src.api.runway.runway_router import router as runway_router
from src.api.slot.slot_router import router as slot_router
from src.api.time_slot.time_slot_router import router as time_slot_router

try:
    from src.api.flight.flight_router import router as flight_router
    _has_flight_router = True
except ImportError:
    flight_router = None
    _has_flight_router = False
    _log = logging.getLogger(__name__)
    _log.warning("Flight router import failed; flights endpoints will not be available")

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

app.include_router(alternative_runway_router, prefix="/alternative_runways", tags=["AlternativeRunway"])
app.include_router(channel_router, prefix="/channels", tags=["Channel"])
app.include_router(interface_router, prefix="/interfaces", tags=["Interface"])
app.include_router(operation_router, prefix="/operations", tags=["Operation"])
app.include_router(resource_router, prefix="/resources", tags=["Resource"])
app.include_router(runway_router, prefix="/runways", tags=["Runway"])
app.include_router(slot_router, prefix="/slots", tags=["Slot"])
app.include_router(time_slot_router, prefix="/time_slots", tags=["TimeSlot"])
if _has_flight_router:
    app.include_router(flight_router, prefix="/flights", tags=["Flight"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")