from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the TransfusionRequest domain class

Package: repository.transfusion_request
Layer: repository
Related tasks: #26, #27, #31
Requirement coverage:
- Accept and Log Transfusion Requests
- Blood Unit Compatibility Matching
- Inventory Dashboard Display
"""

class TransfusionRequestAPI(Protocol):
    ...

class TransfusionRequestDB(Protocol):
    def checkExisting(self, patientDetails: Any, bloodType: Any) -> None:
        ...

    def store(self, requestData: Any) -> None:
        ...

    def assignUniqueID(self, requestID: Any) -> None:
        ...
