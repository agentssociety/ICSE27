from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.load_alert.load_alert_dto import LoadAlertCreate, LoadAlertUpdate, LoadAlertResponse
from src.infra.load_alert.load_alert_repo_impl import SQLAlchemyLoadAlertRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyLoadAlertRepository:
    return SQLAlchemyLoadAlertRepository(db)


@router.get("", response_model=list[LoadAlertResponse])
def list_load_alerts(skip: int = 0, limit: int = 100, repo: SQLAlchemyLoadAlertRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=LoadAlertResponse)
def get_load_alert(item_id: int, repo: SQLAlchemyLoadAlertRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoadAlert not found")
    return item


@router.post("", response_model=LoadAlertResponse, status_code=status.HTTP_201_CREATED)
def create_load_alert(data: LoadAlertCreate, repo: SQLAlchemyLoadAlertRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=LoadAlertResponse)
def update_load_alert(item_id: int, data: LoadAlertUpdate, repo: SQLAlchemyLoadAlertRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoadAlert not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_load_alert(item_id: int, repo: SQLAlchemyLoadAlertRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoadAlert not found")
