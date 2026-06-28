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
from src.api.account_balance.account_balance_router import router as account_balance_router
from src.api.actor.actor_router import router as actor_router
from src.api.audit_log_resource.audit_log_resource_router import router as audit_log_resource_router
from src.api.authentication_attempt.authentication_attempt_router import router as authentication_attempt_router
from src.api.authentication_session.authentication_session_router import router as authentication_session_router
from src.api.card.card_router import router as card_router
from src.api.failed_attempt.failed_attempt_router import router as failed_attempt_router
from src.api.load_alert.load_alert_router import router as load_alert_router
from src.api.lockout_notification.lockout_notification_router import router as lockout_notification_router
from src.api.lockout_record.lockout_record_router import router as lockout_record_router
from src.api.pin.pin_router import router as pin_router
from src.api.storage_state.storage_state_router import router as storage_state_router
from src.api.suspicious_pattern.suspicious_pattern_router import router as suspicious_pattern_router
from src.api.transaction_log.transaction_log_router import router as transaction_log_router
from src.api.transaction_state_change.transaction_state_change_router import router as transaction_state_change_router
from src.api.user.user_router import router as user_router
from src.api.user.admin_router import router as admin_router
from src.api.user_account.user_account_router import router as user_account_router
from src.api.withdrawal_limit.withdrawal_limit_router import router as withdrawal_limit_router
from src.api.withdrawal_request.withdrawal_request_router import router as withdrawal_request_router
from src.api.withdrawal_transaction.withdrawal_transaction_router import router as withdrawal_transaction_router
from src.api.flagged_transaction.flagged_transaction_router import router as flagged_transaction_router

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

app.include_router(account_balance_router, prefix="/account_balances", tags=["AccountBalance"])
app.include_router(actor_router, prefix="/actors", tags=["Actor"])
app.include_router(audit_log_resource_router, prefix="/audit_log_resources", tags=["AuditLogResource"])
app.include_router(authentication_attempt_router, prefix="/authentication_attempts", tags=["AuthenticationAttempt"])
app.include_router(authentication_session_router, prefix="/authentication_sessions", tags=["AuthenticationSession"])
app.include_router(card_router, prefix="/cards", tags=["Card"])
app.include_router(failed_attempt_router, prefix="/failed_attempts", tags=["FailedAttempt"])
app.include_router(load_alert_router, prefix="/load_alerts", tags=["LoadAlert"])
app.include_router(lockout_notification_router, prefix="/lockout_notifications", tags=["LockoutNotification"])
app.include_router(lockout_record_router, prefix="/lockout_records", tags=["LockoutRecord"])
app.include_router(pin_router, prefix="/pins", tags=["Pin"])
app.include_router(storage_state_router, prefix="/storage_states", tags=["StorageState"])
app.include_router(suspicious_pattern_router, prefix="/suspicious_patterns", tags=["SuspiciousPattern"])
app.include_router(transaction_log_router, prefix="/transaction_logs", tags=["TransactionLog"])
app.include_router(transaction_state_change_router, prefix="/transaction_state_changes", tags=["TransactionStateChange"])
app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(user_account_router, prefix="/user_accounts", tags=["UserAccount"])
app.include_router(withdrawal_limit_router, prefix="/withdrawal_limits", tags=["WithdrawalLimit"])
app.include_router(withdrawal_request_router, prefix="/withdrawal_requests", tags=["WithdrawalRequest"])
app.include_router(withdrawal_transaction_router, prefix="/withdrawal_transactions", tags=["WithdrawalTransaction"])
app.include_router(flagged_transaction_router, prefix="/flagged_transactions", tags=["FlaggedTransaction"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
