from __future__ import annotations

from datetime import date
from typing import Optional, Protocol

from src.domain.transfusion_request.TransfusionRequest import TransfusionRequest, RequestStatus
from src.dto.transfusion_request.transfusion_request_dto import TransfusionRequestCreate, TransfusionRequestUpdate, TransfusionRequestResponse
from src.repository.transfusion_request.transfusion_request_repository import TransfusionRequestRepository


class TransfusionRequestService(Protocol):
    """Protocol for transfusion request service operations."""

    def create_request(self, data: TransfusionRequestCreate) -> TransfusionRequestResponse:
        """Create a new transfusion request."""
        ...

    def get_request(self, request_id: int) -> Optional[TransfusionRequestResponse]:
        """Get a transfusion request by ID."""
        ...

    def list_requests(self, skip: int = 0, limit: int = 100) -> list[TransfusionRequestResponse]:
        """List all transfusion requests."""
        ...

    def update_request(self, request_id: int, data: TransfusionRequestUpdate) -> Optional[TransfusionRequestResponse]:
        """Update a transfusion request."""
        ...

    def delete_request(self, request_id: int) -> bool:
        """Delete a transfusion request."""
        ...

    def accept_request(self, request_id: int) -> Optional[TransfusionRequestResponse]:
        """Accept a pending transfusion request."""
        ...


class TransfusionRequestServiceImpl:
    """Service implementation for transfusion request operations."""

    def __init__(self, repository: TransfusionRequestRepository) -> None:
        self._repository = repository

    def create_request(self, data: TransfusionRequestCreate) -> TransfusionRequestResponse:
        domain = TransfusionRequest(
            request_id=data.requestId,
            patient_id=data.patientId,
            patient_abo_rh=data.patientABORh,
            blood_type=data.bloodType,
            request_date=date.today(),
        )
        return self._repository.create(data)

    def get_request(self, request_id: int) -> Optional[TransfusionRequestResponse]:
        return self._repository.get_by_id(request_id)

    def list_requests(self, skip: int = 0, limit: int = 100) -> list[TransfusionRequestResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_request(self, request_id: int, data: TransfusionRequestUpdate) -> Optional[TransfusionRequestResponse]:
        return self._repository.update(request_id, data)

    def delete_request(self, request_id: int) -> bool:
        return self._repository.delete(request_id)

    def accept_request(self, request_id: int) -> Optional[TransfusionRequestResponse]:
        request = self._repository.get_by_id(request_id)
        if request is None:
            return None
        update_data = TransfusionRequestUpdate()
        return self._repository.update(request_id, update_data)

