from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.notification_preference.notification_preference_dto import NotificationPreferenceCreate, NotificationPreferenceUpdate, NotificationPreferenceResponse
from src.infra.notification_preference.notification_preference_repo_impl import SQLAlchemyNotificationPreferenceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyNotificationPreferenceRepository:
    return SQLAlchemyNotificationPreferenceRepository(db)


@router.get("", response_model=list[NotificationPreferenceResponse])
def list_notification_preferences(skip: int = 0, limit: int = 100, repo: SQLAlchemyNotificationPreferenceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=NotificationPreferenceResponse)
def get_notification_preference(item_id: int, repo: SQLAlchemyNotificationPreferenceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NotificationPreference not found")
    return item


@router.post("", response_model=NotificationPreferenceResponse, status_code=status.HTTP_201_CREATED)
def create_notification_preference(data: NotificationPreferenceCreate, repo: SQLAlchemyNotificationPreferenceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=NotificationPreferenceResponse)
def update_notification_preference(item_id: int, data: NotificationPreferenceUpdate, repo: SQLAlchemyNotificationPreferenceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NotificationPreference not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification_preference(item_id: int, repo: SQLAlchemyNotificationPreferenceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NotificationPreference not found")
