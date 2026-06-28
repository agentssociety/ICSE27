from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.account_balance.account_balance_repo_impl import SQLAlchemyAccountBalanceRepository
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.audit_log_resource.audit_log_resource_repo_impl import SQLAlchemyAuditLogResourceRepository
from src.infra.authentication_attempt.authentication_attempt_repo_impl import SQLAlchemyAuthenticationAttemptRepository
from src.infra.authentication_session.authentication_session_repo_impl import SQLAlchemyAuthenticationSessionRepository
from src.infra.card.card_repo_impl import SQLAlchemyCardRepository
from src.infra.failed_attempt.failed_attempt_repo_impl import SQLAlchemyFailedAttemptRepository
from src.infra.load_alert.load_alert_repo_impl import SQLAlchemyLoadAlertRepository
from src.infra.lockout_notification.lockout_notification_repo_impl import SQLAlchemyLockoutNotificationRepository
from src.infra.lockout_record.lockout_record_repo_impl import SQLAlchemyLockoutRecordRepository
from src.infra.pin.pin_repo_impl import SQLAlchemyPinRepository
from src.infra.storage_state.storage_state_repo_impl import SQLAlchemyStorageStateRepository
from src.infra.suspicious_pattern.suspicious_pattern_repo_impl import SQLAlchemySuspiciousPatternRepository
from src.infra.transaction_log.transaction_log_repo_impl import SQLAlchemyTransactionLogRepository
from src.infra.transaction_state_change.transaction_state_change_repo_impl import SQLAlchemyTransactionStateChangeRepository
from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
from src.infra.user_account.user_account_repo_impl import SQLAlchemyUserAccountRepository
from src.infra.withdrawal_limit.withdrawal_limit_repo_impl import SQLAlchemyWithdrawalLimitRepository
from src.infra.withdrawal_request.withdrawal_request_repo_impl import SQLAlchemyWithdrawalRequestRepository
from src.infra.withdrawal_transaction.withdrawal_transaction_repo_impl import SQLAlchemyWithdrawalTransactionRepository


def get_account_balance_repository(db: Session = Depends(get_db)) -> SQLAlchemyAccountBalanceRepository:
    return SQLAlchemyAccountBalanceRepository(db)

def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_audit_log_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogResourceRepository:
    return SQLAlchemyAuditLogResourceRepository(db)

def get_authentication_attempt_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuthenticationAttemptRepository:
    return SQLAlchemyAuthenticationAttemptRepository(db)

def get_authentication_session_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuthenticationSessionRepository:
    return SQLAlchemyAuthenticationSessionRepository(db)

def get_card_repository(db: Session = Depends(get_db)) -> SQLAlchemyCardRepository:
    return SQLAlchemyCardRepository(db)

def get_failed_attempt_repository(db: Session = Depends(get_db)) -> SQLAlchemyFailedAttemptRepository:
    return SQLAlchemyFailedAttemptRepository(db)

def get_load_alert_repository(db: Session = Depends(get_db)) -> SQLAlchemyLoadAlertRepository:
    return SQLAlchemyLoadAlertRepository(db)

def get_lockout_notification_repository(db: Session = Depends(get_db)) -> SQLAlchemyLockoutNotificationRepository:
    return SQLAlchemyLockoutNotificationRepository(db)

def get_lockout_record_repository(db: Session = Depends(get_db)) -> SQLAlchemyLockoutRecordRepository:
    return SQLAlchemyLockoutRecordRepository(db)

def get_pin_repository(db: Session = Depends(get_db)) -> SQLAlchemyPinRepository:
    return SQLAlchemyPinRepository(db)

def get_storage_state_repository(db: Session = Depends(get_db)) -> SQLAlchemyStorageStateRepository:
    return SQLAlchemyStorageStateRepository(db)

def get_suspicious_pattern_repository(db: Session = Depends(get_db)) -> SQLAlchemySuspiciousPatternRepository:
    return SQLAlchemySuspiciousPatternRepository(db)

def get_transaction_log_repository(db: Session = Depends(get_db)) -> SQLAlchemyTransactionLogRepository:
    return SQLAlchemyTransactionLogRepository(db)

def get_transaction_state_change_repository(db: Session = Depends(get_db)) -> SQLAlchemyTransactionStateChangeRepository:
    return SQLAlchemyTransactionStateChangeRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)

def get_user_account_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserAccountRepository:
    return SQLAlchemyUserAccountRepository(db)

def get_withdrawal_limit_repository(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalLimitRepository:
    return SQLAlchemyWithdrawalLimitRepository(db)

def get_withdrawal_request_repository(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalRequestRepository:
    return SQLAlchemyWithdrawalRequestRepository(db)

def get_withdrawal_transaction_repository(db: Session = Depends(get_db)) -> SQLAlchemyWithdrawalTransactionRepository:
    return SQLAlchemyWithdrawalTransactionRepository(db)
