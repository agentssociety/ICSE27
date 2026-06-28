from __future__ import annotations

from src.domain.transfusion_request.TransfusionRequest import (
    RequestState,
    TransfusionRequest,
)


class TestTransfusionRequestDomain:
    """Unit tests for TransfusionRequest domain objects."""

    def test_transfusion_request_default_state(self) -> None:
        req = TransfusionRequest(bloodType="A", rhFactor="positive", quantity=2)
        assert req.bloodType == "A"
        assert req.rhFactor == "positive"
        assert req.quantity == 2
        assert req.state == RequestState.PENDING

    def test_transfusion_request_custom_state(self) -> None:
        req = TransfusionRequest(
            bloodType="O", rhFactor="negative", quantity=1, state=RequestState.VALIDATED
        )
        assert req.state == RequestState.VALIDATED

    def test_request_state_enum_values(self) -> None:
        assert RequestState.PENDING.value == "pending"
        assert RequestState.VALIDATED.value == "validated"
        assert RequestState.STORED.value == "stored"
        assert RequestState.FAILED.value == "failed"

    def test_transfusion_request_invalid_quantity(self) -> None:
        req = TransfusionRequest(bloodType="B", rhFactor="positive", quantity=0)
        assert req.quantity == 0

    def test_transfusion_request_empty_blood_type(self) -> None:
        req = TransfusionRequest(bloodType="", rhFactor="negative", quantity=3)
        assert req.bloodType == ""
