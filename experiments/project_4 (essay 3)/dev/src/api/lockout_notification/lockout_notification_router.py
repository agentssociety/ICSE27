from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.lockout_notification.lockout_notification_dto import LockoutNotificationCreate, LockoutNotificationUpdate, LockoutNotificationResponse
from src.infra.lockout_notification.lockout_notification_repo_impl import SQLAlchemyLockoutNotificationRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyLockoutNotificationRepository:
    return SQLAlchemyLockoutNotificationRepository(db)


@router.get("", response_model=list[LockoutNotificationResponse])
def list_lockout_notifications(skip: int = 0, limit: int = 100, repo: SQLAlchemyLockoutNotificationRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=LockoutNotificationResponse)
def get_lockout_notification(item_id: int, repo: SQLAlchemyLockoutNotificationRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutNotification not found")
    return item


@router.post("", response_model=LockoutNotificationResponse, status_code=status.HTTP_201_CREATED)
def create_lockout_notification(data: LockoutNotificationCreate, repo: SQLAlchemyLockoutNotificationRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=LockoutNotificationResponse)
def update_lockout_notification(item_id: int, data: LockoutNotificationUpdate, repo: SQLAlchemyLockoutNotificationRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutNotification not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lockout_notification(item_id: int, repo: SQLAlchemyLockoutNotificationRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LockoutNotification not found")
