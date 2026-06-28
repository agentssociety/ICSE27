from __future__ import annotations

import pytest
from uuid import UUID, uuid4
from datetime import datetime

from src.domain.transfusion_request.TransfusionRequest import (
    StateEnum,
    Permission,
    PatientDetails,
    BloodType,
    Quantity,
    Urgency,
    UniqueID,
    TransfusionRequest,
    TransfusionRequestId,
    TransfusionRequestCreatedEvent,
    TransfusionRequestUpdatedEvent,
)

"""Unit tests for TransfusionRequest domain

Related tasks: #26, #27, #31
"""


class TestStateEnum:
    def test_state_values(self) -> None:
        assert StateEnum.PENDING.value == "pending"
        assert StateEnum.APPROVED.value == "approved"
        assert StateEnum.MATCHING.value == "matching"
        assert StateEnum.FULFILLED.value == "fulfilled"
        assert StateEnum.CANCELLED.value == "cancelled"


class TestPermission:
    def test_permission_values(self) -> None:
        assert Permission.READ.value == "read"
        assert Permission.WRITE.value == "write"
        assert Permission.ADMIN.value == "admin"


class TestPatientDetails:
    def test_creation_valid(self) -> None:
        details = PatientDetails(
            name="John Doe",
            dateOfBirth="1990-01-01",
            medicalRecordNumber="MRN-001",
        )
        assert details.name == "John Doe"
        assert details.dateOfBirth == "1990-01-01"
        assert details.medicalRecordNumber == "MRN-001"

    def test_creation_empty_name(self) -> None:
        with pytest.raises(ValueError, match="Patient name cannot be empty"):
            PatientDetails(name="", dateOfBirth="1990-01-01", medicalRecordNumber="MRN-001")

    def test_creation_empty_mrn(self) -> None:
        with pytest.raises(ValueError, match="Medical record number cannot be empty"):
            PatientDetails(name="John Doe", dateOfBirth="1990-01-01", medicalRecordNumber="")

    def test_update_details(self) -> None:
        details = PatientDetails(
            name="John Doe",
            dateOfBirth="1990-01-01",
            medicalRecordNumber="MRN-001",
        )
        details.updateDetails(name="Jane Doe", dateOfBirth="1995-05-05")
        assert details.name == "Jane Doe"
        assert details.dateOfBirth == "1995-05-05"
        assert details.medicalRecordNumber == "MRN-001"  # Unchanged

    def test_update_details_invalid_name(self) -> None:
        details = PatientDetails(
            name="John Doe",
            dateOfBirth="1990-01-01",
            medicalRecordNumber="MRN-001",
        )
        with pytest.raises(ValueError, match="Patient name cannot be empty"):
            details.updateDetails(name="")


class TestBloodType:
    def test_creation_valid(self) -> None:
        bt = BloodType(type="A+")
        assert bt.type == "A+"

    def test_creation_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="Invalid blood type"):
            BloodType(type="X+")


class TestQuantity:
    def test_creation_valid(self) -> None:
        qty = Quantity(units=5)
        assert qty.units == 5

    def test_creation_zero(self) -> None:
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Quantity(units=0)

    def test_creation_negative(self) -> None:
        with pytest.raises(ValueError, match="Quantity must be positive"):
            Quantity(units=-1)

    def test_creation_exceeds_max(self) -> None:
        with pytest.raises(ValueError, match="Quantity exceeds maximum allowed"):
            Quantity(units=101)


class TestUrgency:
    def test_creation_valid(self) -> None:
        urg = Urgency(level="high")
        assert urg.level == "high"

    def test_creation_invalid_level(self) -> None:
        with pytest.raises(ValueError, match="Invalid urgency level"):
            Urgency(level="urgent")


class TestUniqueID:
    def test_generate(self) -> None:
        uid = UniqueID.generate()
        assert isinstance(uid.id, UUID)

    def test_uniqueness(self) -> None:
        uid1 = UniqueID.generate()
        uid2 = UniqueID.generate()
        assert uid1.id != uid2.id


class TestTransfusionRequest:
    def test_creation_valid(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        assert request.state == StateEnum.PENDING
        assert request.duplicateFlag is False
        assert request.created_at is not None

    def test_back_references(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="O-"),
            quantity=Quantity(units=2),
            urgency=Urgency(level="critical"),
        )
        assert request.patientDetails.transfusionRequest is request
        assert request.bloodType.transfusionRequest is request
        assert request.quantity.transfusionRequest is request
        assert request.urgency.transfusionRequest is request

    def test_duplicate_flag(self) -> None:
        with pytest.raises(ValueError, match="Duplicate transfusion request detected"):
            TransfusionRequest(
                uniqueID=UniqueID.generate(),
                patientDetails=PatientDetails(
                    name="John Doe",
                    dateOfBirth="1990-01-01",
                    medicalRecordNumber="MRN-001",
                ),
                bloodType=BloodType(type="A+"),
                quantity=Quantity(units=3),
                urgency=Urgency(level="high"),
                duplicateFlag=True,
            )

    def test_is_duplicate_true(self) -> None:
        request1 = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request2 = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="low"),
        )
        assert request1.isDuplicate(request2) is True

    def test_is_duplicate_false_different_mrn(self) -> None:
        request1 = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request2 = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="Jane Doe",
                dateOfBirth="1995-05-05",
                medicalRecordNumber="MRN-002",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        assert request1.isDuplicate(request2) is False

    def test_update_state_valid(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request.updateState(StateEnum.APPROVED)
        assert request.state == StateEnum.APPROVED
        request.updateState(StateEnum.MATCHING)
        assert request.state == StateEnum.MATCHING
        request.updateState(StateEnum.FULFILLED)
        assert request.state == StateEnum.FULFILLED

    def test_update_state_invalid(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        # Cannot go from PENDING directly to FULFILLED
        with pytest.raises(ValueError, match="Invalid state transition"):
            request.updateState(StateEnum.FULFILLED)

    def test_update_state_from_completed(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request.updateState(StateEnum.APPROVED)
        request.updateState(StateEnum.MATCHING)
        request.updateState(StateEnum.FULFILLED)
        # Fulfilled requests cannot be changed
        with pytest.raises(ValueError, match="Invalid state transition"):
            request.updateState(StateEnum.CANCELLED)

    def test_can_fulfill_true(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request.updateState(StateEnum.APPROVED)
        request.updateState(StateEnum.MATCHING)
        assert request.canFulfill(available_units=5) is True

    def test_can_fulfill_false_not_matching(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        # Request is still PENDING
        assert request.canFulfill(available_units=5) is False

    def test_can_fulfill_false_insufficient_units(self) -> None:
        request = TransfusionRequest(
            uniqueID=UniqueID.generate(),
            patientDetails=PatientDetails(
                name="John Doe",
                dateOfBirth="1990-01-01",
                medicalRecordNumber="MRN-001",
            ),
            bloodType=BloodType(type="A+"),
            quantity=Quantity(units=3),
            urgency=Urgency(level="high"),
        )
        request.updateState(StateEnum.APPROVED)
        request.updateState(StateEnum.MATCHING)
        assert request.canFulfill(available_units=2) is False


class TestTransfusionRequestId:
    def test_creation(self) -> None:
        req_id = TransfusionRequestId(id="req-001")
        assert req_id.id == "req-001"


class TestTransfusionRequestEvents:
    def test_created_event(self) -> None:
        req_id = TransfusionRequestId(id="req-001")
        event = TransfusionRequestCreatedEvent(request_id=req_id)
        assert event.request_id.id == "req-001"
        assert event.timestamp is not None

    def test_updated_event(self) -> None:
        req_id = TransfusionRequestId(id="req-001")
        event = TransfusionRequestUpdatedEvent(request_id=req_id)
        assert event.request_id.id == "req-001"
        assert event.timestamp is not None
