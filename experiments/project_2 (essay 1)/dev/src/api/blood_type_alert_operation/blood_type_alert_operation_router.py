from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.blood_type_alert_operation.blood_type_alert_operation_dto import (
    BloodTypeAlertOperationCreate,
    BloodTypeAlertOperationUpdate,
    BloodTypeAlertOperationResponse,
)
from src.infra.blood_type_alert_operation.blood_type_alert_operation_repo_impl import (
    SQLAlchemyBloodTypeAlertOperationRepository,
)


router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBloodTypeAlertOperationRepository:
    return SQLAlchemyBloodTypeAlertOperationRepository(db)


@router.get("", response_model=list[BloodTypeAlertOperationResponse])
def list_blood_type_alert_operations(
    skip: int = 0,
    limit: int = 100,
    repo: SQLAlchemyBloodTypeAlertOperationRepository = Depends(_repo),
):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BloodTypeAlertOperationResponse)
def get_blood_type_alert_operation(
    item_id: int,
    repo: SQLAlchemyBloodTypeAlertOperationRepository = Depends(_repo),
):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BloodTypeAlertOperation not found",
        )
    return item


@router.post(
    "", response_model=BloodTypeAlertOperationResponse, status_code=status.HTTP_201_CREATED
)
def create_blood_type_alert_operation(
    data: BloodTypeAlertOperationCreate,
    repo: SQLAlchemyBloodTypeAlertOperationRepository = Depends(_repo),
):
    return repo.create(data)


@router.put("/{item_id}", response_model=BloodTypeAlertOperationResponse)
def update_blood_type_alert_operation(
    item_id: int,
    data: BloodTypeAlertOperationUpdate,
    repo: SQLAlchemyBloodTypeAlertOperationRepository = Depends(_repo),
):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BloodTypeAlertOperation not found",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_type_alert_operation(
    item_id: int,
    repo: SQLAlchemyBloodTypeAlertOperationRepository = Depends(_repo),
):
    if not repo.delete(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BloodTypeAlertOperation not found",
        )
