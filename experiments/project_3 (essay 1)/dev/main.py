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

# Actor router not available in this project

try:
    from src.api.aircraft.aircraft_router import router as aircraft_router
except ModuleNotFoundError:
    aircraft_router = None
    logging.getLogger(__name__).warning("aircraft_router not available")

try:
    from src.api.flight.flight_router import router as flight_router
except ModuleNotFoundError:
    flight_router = None
    logging.getLogger(__name__).warning("flight_router not available")

try:
    from src.api.interface.interface_router import router as interface_router
except ModuleNotFoundError:
    interface_router = None
    logging.getLogger(__name__).warning("interface_router not available")

try:
    from src.api.operation.operation_router import router as operation_router
except ModuleNotFoundError:
    operation_router = None
    logging.getLogger(__name__).warning("operation_router not available")

try:
    from src.api.operation_slot.operation_slot_router import router as operation_slot_router
except ModuleNotFoundError:
    operation_slot_router = None
    logging.getLogger(__name__).warning("operation_slot_router not available")

try:
    from src.api.permission.permission_router import router as permission_router
except ModuleNotFoundError:
    permission_router = None
    logging.getLogger(__name__).warning("permission_router not available")

try:
    from src.api.resource.resource_router import router as resource_router
except ModuleNotFoundError:
    resource_router = None
    logging.getLogger(__name__).warning("resource_router not available")

try:
    from src.api.runway.runway_router import router as runway_router
except ModuleNotFoundError:
    runway_router = None
    logging.getLogger(__name__).warning("runway_router not available")

try:
    from src.api.separation_rule.separation_rule_router import router as separation_rule_router
except ModuleNotFoundError:
    separation_rule_router = None
    logging.getLogger(__name__).warning("separation_rule_router not available")

try:
    from src.api.slot.slot_router import router as slot_router
except ModuleNotFoundError:
    slot_router = None
    logging.getLogger(__name__).warning("slot_router not available")

try:
    from src.api.state.state_router import router as state_router
except ModuleNotFoundError:
    state_router = None
    logging.getLogger(__name__).warning("state_router not available")

try:
    from src.api.traffic_data.traffic_data_router import router as traffic_data_router
except ModuleNotFoundError:
    traffic_data_router = None
    logging.getLogger(__name__).warning("traffic_data_router not available")

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

# actor_router not available in this project
if aircraft_router is not None:
    app.include_router(aircraft_router, prefix="/aircrafts", tags=["Aircraft"])
if flight_router is not None:
    app.include_router(flight_router, prefix="/flights", tags=["Flight"])
if interface_router is not None:
    app.include_router(interface_router, prefix="/interfaces", tags=["Interface"])
if operation_router is not None:
    app.include_router(operation_router, prefix="/operations", tags=["Operation"])
if operation_slot_router is not None:
    app.include_router(operation_slot_router, prefix="/operation_slots", tags=["OperationSlot"])
if permission_router is not None:
    app.include_router(permission_router, prefix="/permissions", tags=["Permission"])
if resource_router is not None:
    app.include_router(resource_router, prefix="/resources", tags=["Resource"])
if runway_router is not None:
    app.include_router(runway_router, prefix="/runways", tags=["Runway"])
if separation_rule_router is not None:
    app.include_router(separation_rule_router, prefix="/separation_rules", tags=["SeparationRule"])
if slot_router is not None:
    app.include_router(slot_router, prefix="/slots", tags=["Slot"])
if state_router is not None:
    app.include_router(state_router, prefix="/states", tags=["State"])
if traffic_data_router is not None:
    app.include_router(traffic_data_router, prefix="/traffic_datas", tags=["TrafficData"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=8766, log_level="info")