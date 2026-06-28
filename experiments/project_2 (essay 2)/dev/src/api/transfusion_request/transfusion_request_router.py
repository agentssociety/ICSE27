from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.transfusion_request.transfusion_request_dto import (
    TransfusionRequestDTO,
    ValidationResult,
    StorageResult,
    Response,
)
from src.infra.transfusion_request.transfusion_request_repo_impl import (
    SQLAlchemyTransfusionRequestRepository,
)

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyTransfusionRequestRepository:
    return SQLAlchemyTransfusionRequestRepository(db)


ALLOWED_BLOOD_TYPES = {"A", "B", "AB", "O"}
ALLOWED_RH_FACTORS = {"positive", "negative"}


@router.post("/validate", response_model=ValidationResult)
def validate_request(data: TransfusionRequestDTO, repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo)):
    """Validate transfusion request parameters."""
    validation = repo.validate_request(data)
    return validation


@router.post("", response_model=StorageResult, status_code=status.HTTP_201_CREATED)
def submit_request(data: TransfusionRequestDTO, repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo)):
    """Submit a transfusion request after validation."""
    result = repo.store_request(data)
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.errorMessage)
    return result


@router.get("/{request_id}", response_model=TransfusionRequestDTO)
def get_request(request_id: int, repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo)):
    """Get a stored transfusion request by ID."""
    item = repo.get_by_id(request_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfusion request not found")
    return item


@router.get("", response_model=list[TransfusionRequestDTO])
def list_requests(skip: int = 0, limit: int = 100, repo: SQLAlchemyTransfusionRequestRepository = Depends(_repo)):
    """List all stored transfusion requests."""
    return repo.get_all(skip=skip, limit=limit)
