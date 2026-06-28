from __future__ import annotations

from datetime import date

import pytest

from src.domain.transfusion_request.TransfusionRequest import TransfusionRequest, RequestStatus


class TestTransfusionRequestDomain:
    def test_create_request(self) -> None:
        request = TransfusionRequest(
            request_id="REQ-001",
            patient_id="PAT-001",
            patient_abo_rh="A+",
            blood_type="A+",
            request_date=date(2024, 1, 15),
        )
        assert request.request_id == "REQ-001"
        assert request.patient_id == "PAT-001"
        assert request.status == RequestStatus.PENDING

    def test_accept_request(self) -> None:
        request = TransfusionRequest(
            request_id="REQ-001",
            patient_id="PAT-001",
            patient_abo_rh="A+",
            blood_type="A+",
            request_date=date(2024, 1, 15),
        )
        request.accept()
        assert request.status == RequestStatus.ACCEPTED

    def test_process_request(self) -> None:
        request = TransfusionRequest(
            request_id="REQ-001",
            patient_id="PAT-001",
            patient_abo_rh="A+",
            blood_type="A+",
            request_date=date(2024, 1, 15),
        )
        request.process()
        assert request.status == RequestStatus.PROCESSING

    def test_complete_request(self) -> None:
        request = TransfusionRequest(
            request_id="REQ-001",
            patient_id="PAT-001",
            patient_abo_rh="A+",
            blood_type="A+",
            request_date=date(2024, 1, 15),
        )
        request.complete()
        assert request.status == RequestStatus.COMPLETED

    def test_cancel_request(self) -> None:
        request = TransfusionRequest(
            request_id="REQ-001",
            patient_id="PAT-001",
            patient_abo_rh="A+",
            blood_type="A+",
            request_date=date(2024, 1, 15),
        )
        request.cancel()
        assert request.status == RequestStatus.CANCELLED
