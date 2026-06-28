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
from src.api.actor.actor_router import router as actor_router
from src.api.flight.flight_router import router as flight_router
from src.api.interface.interface_router import router as interface_router
from src.api.resource.resource_router import router as resource_router
from src.api.runway.runway_router import router as runway_router

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
app.include_router(flight_router, prefix="/flights", tags=["Flight"])
app.include_router(interface_router, prefix="/interfaces", tags=["Interface"])
app.include_router(resource_router, prefix="/resources", tags=["Resource"])
app.include_router(runway_router, prefix="/runways", tags=["Runway"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
