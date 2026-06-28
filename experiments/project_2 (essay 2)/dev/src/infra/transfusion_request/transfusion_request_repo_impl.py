from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.transfusion_request.transfusion_request_dto import (
    TransfusionRequestDTO,
    StorageResult,
    ValidationResult,
    Response,
)
from src.orm.transfusion_request.transfusion_request_orm import (
    TransfusionRequestORM,
    TransfusionRequestStatus,
)


class SQLAlchemyTransfusionRequestRepository:
    """Repository for storing and retrieving transfusion requests using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def validate_request(self, dto: TransfusionRequestDTO) -> ValidationResult:
        """Validate a transfusion request parameters."""
        if not dto.bloodType or dto.bloodType not in ("A", "B", "AB", "O"):
            return ValidationResult(isValid=False, errorMessage="Invalid blood type. Must be A, B, AB, or O.")
        if not dto.rhFactor or dto.rhFactor not in ("positive", "negative"):
            return ValidationResult(isValid=False, errorMessage="Invalid Rh factor. Must be positive or negative.")
        if dto.quantity <= 0:
            return ValidationResult(isValid=False, errorMessage="Quantity must be positive.")
        return ValidationResult(isValid=True, errorMessage="")

    def store_request(self, dto: TransfusionRequestDTO) -> StorageResult:
        """Validate and store a transfusion request."""
        validation = self.validate_request(dto)
        if not validation.isValid:
            return StorageResult(success=False, requestId="", errorMessage=validation.errorMessage)

        row = TransfusionRequestORM(
            patient_id="pending",
            blood_type=dto.bloodType,
            rh_factor=dto.rhFactor,
            units_required=dto.quantity,
            priority="normal",
            status=TransfusionRequestStatus.PENDING,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StorageResult(success=True, requestId=str(row.id), errorMessage="")

    def get_by_id(self, request_id: int) -> Optional[TransfusionRequestDTO]:
        """Retrieve a stored request by ID."""
        row = self._session.get(TransfusionRequestORM, request_id)
        if row is None:
            return None
        return TransfusionRequestDTO(
            bloodType=row.blood_type,
            rhFactor=row.rh_factor,
            quantity=row.units_required,
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransfusionRequestDTO]:
        """List stored requests."""
        rows = self._session.query(TransfusionRequestORM).offset(skip).limit(limit).all()
        return [
            TransfusionRequestDTO(
                bloodType=r.blood_type,
                rhFactor=r.rh_factor,
                quantity=r.units_required,
            )
            for r in rows
        ]
