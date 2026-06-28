from __future__ import annotations

from typing import Optional, Protocol

from src.dto.transfusion_request.transfusion_request_dto import (
    TransfusionRequestDTO,
    ValidationResult,
    StorageResult,
    Response,
)


class TransfusionRequestDatabase(Protocol):
    """Interface for storing and retrieving transfusion requests."""

    def store_request(self, dto: TransfusionRequestDTO) -> StorageResult:
        """Validate and store a transfusion request."""
        ...

    def get_by_id(self, request_id: int) -> Optional[TransfusionRequestDTO]:
        """Retrieve a stored request by ID."""
        ...

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransfusionRequestDTO]:
        """List stored requests."""
        ...
