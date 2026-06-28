from __future__ import annotations

from typing import Any, TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.account.account_dto import (
    LoginRequestDTO, LoginResponseDTO, LockStatus,
    UnlockRequestDTO, UnlockResponseDTO,
    AuthorizationRequest, AuthorizationResponse,
    AccountData
)
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository

if TYPE_CHECKING:
    from src.service.account import LockUnlockService

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAccountRepository:
    return SQLAlchemyAccountRepository(db)


@router.post("/login", response_model=LoginResponseDTO)
def login(request: LoginRequestDTO, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    # Simple login check
    account = repo.get_by_id(request.userId)
    if account is None:
        return LoginResponseDTO(success=False, lockStatus=LockStatus.UNLOCKED, message="Account not found")
    
    if account.lock_status == "locked":
        return LoginResponseDTO(success=False, lockStatus=LockStatus.LOCKED, message="Account is locked")
    
    # PIN verification (simplified)
    if request.pin == "1234":  # Mock PIN check
        repo.reset_failed_attempts(request.userId)
        return LoginResponseDTO(success=True, lockStatus=LockStatus.UNLOCKED, message="Login successful")
    else:
        repo.record_failed_attempt(request.userId)
        account = repo.get_by_id(request.userId)
        is_locked = account is not None and account.lock_status == "locked"
        new_status = LockStatus.LOCKED if is_locked else LockStatus.UNLOCKED
        return LoginResponseDTO(
            success=False,
            lockStatus=new_status,
            message="Invalid PIN" if not is_locked else "Account locked due to multiple failed attempts"
        )


@router.post("/unlock", response_model=UnlockResponseDTO)
def unlock(request: UnlockRequestDTO, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    # Admin unlock
    if repo.unlock_account(request.userId):
        return UnlockResponseDTO(success=True, message="Account unlocked")
    return UnlockResponseDTO(success=False, message="Account not found")


@router.post("/authorize", response_model=AuthorizationResponse)
def authorize(request: AuthorizationRequest, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    account = repo.get_by_id(request.accountId)
    if account is None:
        return AuthorizationResponse(authorized=False, newBalance=0, newUsedToday=0, reason="Account not found")
    
    if account.lock_status == "locked":
        return AuthorizationResponse(authorized=False, newBalance=account.balance, newUsedToday=account.used_today, reason="Account is locked")
    
    if account.balance < request.amount:
        return AuthorizationResponse(authorized=False, newBalance=account.balance, newUsedToday=account.used_today, reason="Insufficient funds")
    
    if account.used_today + request.amount > account.daily_limit:
        return AuthorizationResponse(authorized=False, newBalance=account.balance, newUsedToday=account.used_today, reason="Daily limit exceeded")
    
    return AuthorizationResponse(authorized=True, newBalance=account.balance - request.amount, newUsedToday=account.used_today + request.amount, reason="Authorized")


@router.get("/{account_id}/balance", response_model=AccountData)
def get_balance(account_id: str, repo: SQLAlchemyAccountRepository = Depends(_repo)):
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return AccountData(balance=account.balance, dailyLimit=account.daily_limit, usedToday=account.used_today)


class LoginController:
    def __init__(self, loginService: Any = None) -> None:
        self.loginService = loginService

    def handleLoginRequest(self, userId: str, pin: str) -> None:
        pass


class AdminController:
    def __init__(self, adminService: Any = None) -> None:
        self.adminService = adminService

    def handleUnlockRequest(self, userId: str, adminId: str) -> None:
        pass


class AccountController:
    def __init__(self, lockUnlockService: Any = None) -> None:
        self.lockUnlockService = lockUnlockService
