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

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        _log.info("Database tables created / verified.")
    except Exception as exc:
        _log.warning("DB unavailable at startup (will retry per request): %s", exc)

    # Defer imports to break circular dependencies
    from src.api.account.account_router import router as account_router
    from src.api.actor.actor_router import router as actor_router
    from src.api.audit_log_entry.audit_log_entry_router import router as audit_log_entry_router
    from src.api.card.card_router import router as card_router
    from src.api.money.money_router import router as money_router
    from src.api.pin.pin_router import router as pin_router
    from src.api.transaction.transaction_router import router as transaction_router
    from src.api.user.user_router import router as user_router
    from src.api.withdrawal_record.withdrawal_record_router import router as withdrawal_record_router

    app.include_router(account_router, prefix="/accounts", tags=["Account"])
    app.include_router(actor_router, prefix="/actors", tags=["Actor"])
    app.include_router(audit_log_entry_router, prefix="/audit_logs", tags=["AuditLogEntry"])
    app.include_router(card_router, prefix="/cards", tags=["Card"])
    app.include_router(money_router, prefix="/moneys", tags=["Money"])
    app.include_router(pin_router, prefix="/pins", tags=["PIN"])
    app.include_router(transaction_router, prefix="/transactions", tags=["Transaction"])
    app.include_router(user_router, prefix="/users", tags=["User"])
    app.include_router(withdrawal_record_router, prefix="/withdrawal_records", tags=["WithdrawalRecord"])

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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
