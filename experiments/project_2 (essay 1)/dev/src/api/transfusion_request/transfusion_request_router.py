from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transfusion_request.transfusion_request_dto import (
    TransfusionRequestCreateRequest,
    TransfusionRequestUpdateRequest,
    TransfusionRequestResponse,
)
from src.infra.transfusion_request.transfusion_request_repo_impl import SQLAlchemyTransfusionRequestRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransfusionRequestRepository:
    return SQLAlchemyTransfusionRequestRepository(db)


@router.get("", response_model=list[TransfusionRequestResponse])
def list_transfusion_requests(
    skip: int = 0,
    limit: int = 100,
    repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo),
):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=TransfusionRequestResponse)
def get_transfusion_request(
    item_id: int,
    repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo),
):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransfusionRequest not found")
    return item


@router.post("", response_model=TransfusionRequestResponse, status_code=status.HTTP_201_CREATED)
def create_transfusion_request(
    data: TransfusionRequestCreateRequest,
    repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo),
):
    return repo.create(data)


@router.put("/{item_id}", response_model=TransfusionRequestResponse)
def update_transfusion_request(
    item_id: int,
    data: TransfusionRequestUpdateRequest,
    repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo),
):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransfusionRequest not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transfusion_request(
    item_id: int,
    repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo),
):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TransfusionRequest not found")
