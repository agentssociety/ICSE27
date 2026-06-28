from __future__ import annotations

import pytest
from datetime import datetime, timezone
from src.domain.patient.Patient import Patient, PatientRecord, SymptomData, QueueEntry


class TestPatientDomain:
    def test_patient_creation(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="fever, cough",
            urgencyLevel=5,
            queuePosition=1,
            arrivalTime=now,
            urgency="5",
        )
        assert patient.symptoms == "fever, cough"
        assert patient.urgencyLevel == 5
        assert patient.queuePosition == 1
        assert patient.urgency == "5"

    def test_assign_urgency_valid(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="pain",
            urgencyLevel=5,
            queuePosition=1,
            arrivalTime=now,
            urgency="5",
        )
        patient.assignUrgency(2)
        assert patient.urgencyLevel == 2
        assert patient.urgency == "2"

    def test_assign_urgency_invalid_low(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="pain",
            urgencyLevel=5,
            queuePosition=1,
            arrivalTime=now,
            urgency="5",
        )
        with pytest.raises(ValueError, match="must be between 1 and 5"):
            patient.assignUrgency(0)

    def test_assign_urgency_invalid_high(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="pain",
            urgencyLevel=5,
            queuePosition=1,
            arrivalTime=now,
            urgency="5",
        )
        with pytest.raises(ValueError, match="must be between 1 and 5"):
            patient.assignUrgency(6)

    def test_update_urgency(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="pain",
            urgencyLevel=5,
            queuePosition=1,
            arrivalTime=now,
            urgency="5",
        )
        patient.updateUrgency("1")
        assert patient.urgency == "1"

    def test_get_details(self) -> None:
        now = datetime.now(timezone.utc)
        patient = Patient(
            symptoms="headache",
            urgencyLevel=3,
            queuePosition=2,
            arrivalTime=now,
            urgency="3",
        )
        details = patient.getDetails()
        assert details["symptoms"] == "headache"
        assert details["urgencyLevel"] == 3
        assert details["queuePosition"] == 2
        assert details["urgency"] == "3"

    def test_create_patient_record(self) -> None:
        from src.domain.patient.Patient import Actor, Permission
        actor = Actor(mayPerform={Permission.READ})
        record = PatientRecord(owner=actor, accessible={actor})
        result = record.createPatientRecord({"name": "test"})
        assert result.owner == actor
        assert actor in result.accessible

    def test_create_symptom_data(self) -> None:
        from src.domain.patient.Patient import Actor, Permission
        actor = Actor(mayPerform={Permission.READ})
        sd = SymptomData(owner=actor, accessible={actor})
        result = sd.createSymptomData("fever", "pat-1")
        assert result.owner == actor

    def test_create_queue_entry(self) -> None:
        from src.domain.patient.Patient import Actor, Permission
        actor = Actor(mayPerform={Permission.READ})
        qe = QueueEntry(owner=actor, accessible={actor})
        result = qe.createQueueEntry("pat-1", "waiting")
        assert result.owner == actor
