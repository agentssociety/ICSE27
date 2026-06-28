from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.patient.Patient import (
    Patient, Symptom, SymptomRecord, UserAuthenticationSystem,
    Permission, SymptomState
)


class TestPatientDomain:
    def test_symptom_create(self):
        """Test that Symptom.create works correctly."""
        auth = UserAuthenticationSystem(sessionToken="tok123", userId="user1", patient=None)  # type: ignore
        patient = Patient(username="testuser", authentication=auth)
        auth.patient = patient

        symptom = Symptom.create(
            description="Headache",
            language="en",
            patientId="user1",
            patient=patient,
        )

        assert symptom.description == "Headache"
        assert symptom.language == "en"
        assert symptom.patientId == "user1"
        assert symptom.patient == patient
        assert isinstance(symptom.timestamp, datetime)

    def test_symptom_record_map_to_record(self):
        """Test SymptomRecord.mapToRecord conversion."""
        auth = UserAuthenticationSystem(sessionToken="tok123", userId="user1", patient=None)  # type: ignore
        patient = Patient(username="testuser", authentication=auth)
        auth.patient = patient

        symptom = Symptom.create(description="Fever", language="en", patientId="user1", patient=patient)
        record = SymptomRecord.mapToRecord(symptom)

        assert record.symptom == symptom
        assert record.patientId == "user1"
        assert symptom.description in record.symptomData
        assert isinstance(record.storedAt, datetime)
        assert isinstance(record.recordId, str)

    def test_input_symptoms_creates_record(self):
        """When patient registers symptoms, a SymptomRecord is created."""
        auth = UserAuthenticationSystem(sessionToken="tok123", userId="user1", patient=None)  # type: ignore
        patient = Patient(username="testuser", authentication=auth)
        auth.patient = patient

        record = patient.inputSymptoms(description="Cough", language="en")

        assert isinstance(record, SymptomRecord)
        assert record.patientId == "user1"
        assert "Cough" in record.symptomData

    def test_authenticate_success(self):
        """Valid session token returns userId."""
        auth = UserAuthenticationSystem(sessionToken="valid_token", userId="u1", patient=None)  # type: ignore
        result = auth.authenticate("valid_token")
        assert result == "u1"

    def test_authenticate_failure(self):
        """Invalid session token raises PermissionError."""
        auth = UserAuthenticationSystem(sessionToken="valid_token", userId="u1", patient=None)  # type: ignore
        with pytest.raises(PermissionError):
            auth.authenticate("wrong_token")

    def test_display_methods(self):
        """UI display methods should not raise errors."""
        auth = UserAuthenticationSystem(sessionToken="t", userId="u", patient=None)  # type: ignore
        patient = Patient(username="test", authentication=auth)
        auth.patient = patient

        # Just ensure no exception
        patient.displayConfirmation("ok")
        patient.displayMessage("msg")
        patient.displayError("err")
        patient.retryOnReconnection()

    def test_set_encrypted_at_rest(self):
        """setEncryptedAtRest should not raise."""
        auth = UserAuthenticationSystem(sessionToken="t", userId="u", patient=None)  # type: ignore
        patient = Patient(username="test", authentication=auth)
        auth.patient = patient
        symptom = Symptom.create(description="A", language="en", patientId="u", patient=patient)
        record = SymptomRecord.mapToRecord(symptom)
        record.setEncryptedAtRest()  # should not raise

    def test_enums(self):
        """Enums have expected values."""
        assert Permission.WRITE.value == "write"
        assert Permission.READ.value == "read"
        assert Permission.ADMIN.value == "admin"
        assert SymptomState.PRE1.value == "pre1"
        assert SymptomState.POST2.value == "post2"
