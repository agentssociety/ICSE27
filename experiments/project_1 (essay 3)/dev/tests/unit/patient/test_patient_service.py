from __future__ import annotations

import pytest
from src.domain.patient.Patient import Patient, UserAuthenticationSystem
from src.service.patient.patient_service import PatientSymptomService


class TestPatientSymptomService:
    def test_register_symptom_success(self):
        auth = UserAuthenticationSystem(sessionToken="tok123", userId="user1", patient=None)  # type: ignore
        patient = Patient(username="testuser", authentication=auth)
        auth.patient = patient

        service = PatientSymptomService()
        service.add_patient(patient)

        record = service.register_symptom(
            username="testuser",
            session_token="tok123",
            description="Headache",
            language="en"
        )

        assert record.patientId == "user1"
        assert "Headache" in record.symptomData

    def test_register_symptom_patient_not_found(self):
        service = PatientSymptomService()
        with pytest.raises(ValueError, match="not found"):
            service.register_symptom(
                username="nonexistent",
                session_token="tok",
                description="A",
                language="en"
            )

    def test_register_symptom_authentication_failure(self):
        auth = UserAuthenticationSystem(sessionToken="real_token", userId="user1", patient=None)  # type: ignore
        patient = Patient(username="testuser", authentication=auth)
        auth.patient = patient

        service = PatientSymptomService()
        service.add_patient(patient)

        with pytest.raises(PermissionError):
            service.register_symptom(
                username="testuser",
                session_token="wrong_token",
                description="Pain",
                language="en"
            )
