from __future__ import annotations

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, timezone, timedelta

from src.dto.patient.patient_dto import PatientCreate, PatientResponse
from src.service.patient.patient_service import PatientServiceImpl


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return PatientServiceImpl(repository=mock_repo)


class TestPatientService:
    def test_register_patient_with_symptoms_creates_patient(self, service, mock_repo):
        mock_repo.create.return_value = PatientResponse(
            id=1,
            symptoms="fever, cough",
            urgencyLevel=5,
            queuePosition=0,
            arrivalTime=datetime.now(timezone.utc),
            urgency="5",
        )
        mock_repo.get_all.return_value = [mock_repo.create.return_value]
        result = service.register_patient_with_symptoms("fever, cough")
        assert result.symptoms == "fever, cough"
        assert result.urgencyLevel == 5
        assert mock_repo.create.called

    def test_register_patient_sets_default_urgency(self, service, mock_repo):
        mock_repo.create.return_value = PatientResponse(
            id=2,
            symptoms="pain",
            urgencyLevel=5,
            queuePosition=0,
            arrivalTime=datetime.now(timezone.utc),
            urgency="5",
        )
        mock_repo.get_all.return_value = [mock_repo.create.return_value]
        result = service.register_patient_with_symptoms("pain")
        assert result.urgencyLevel == 5
        assert result.urgency == "5"

    def test_assign_urgency_valid(self, service, mock_repo):
        mock_repo.update.return_value = PatientResponse(
            id=1,
            symptoms="fever",
            urgencyLevel=2,
            queuePosition=0,
            arrivalTime=datetime.now(timezone.utc),
            urgency="2",
        )
        mock_repo.get_all.return_value = [mock_repo.update.return_value]
        result = service.assign_urgency(1, 2)
        assert result.urgencyLevel == 2
        assert result.urgency == "2"
        assert mock_repo.update.called

    def test_assign_urgency_invalid_low(self, service, mock_repo):
        with pytest.raises(ValueError, match="must be between 1 and 5"):
            service.assign_urgency(1, 0)

    def test_assign_urgency_invalid_high(self, service, mock_repo):
        with pytest.raises(ValueError, match="must be between 1 and 5"):
            service.assign_urgency(1, 6)

    def test_assign_urgency_patient_not_found(self, service, mock_repo):
        mock_repo.update.return_value = None
        with pytest.raises(ValueError, match="not found"):
            service.assign_urgency(999, 3)

    def test_get_sorted_queue_returns_sorted_by_urgency_then_time(self, service, mock_repo):
        base_time = datetime.now(timezone.utc)
        mock_repo.get_all.return_value = [
            PatientResponse(id=1, symptoms="a", urgencyLevel=3, queuePosition=1, arrivalTime=base_time, urgency="3"),
            PatientResponse(id=2, symptoms="b", urgencyLevel=1, queuePosition=2, arrivalTime=base_time + timedelta(minutes=1), urgency="1"),
            PatientResponse(id=3, symptoms="c", urgencyLevel=2, queuePosition=3, arrivalTime=base_time + timedelta(minutes=2), urgency="2"),
        ]
        result = service.get_sorted_queue()
        assert result[0].id == 2  # urgency 1
        assert result[1].id == 3  # urgency 2
        assert result[2].id == 1  # urgency 3

    def test_get_sorted_queue_same_urgency_by_time(self, service, mock_repo):
        base_time = datetime.now(timezone.utc)
        mock_repo.get_all.return_value = [
            PatientResponse(id=1, symptoms="a", urgencyLevel=2, queuePosition=1, arrivalTime=base_time + timedelta(minutes=5), urgency="2"),
            PatientResponse(id=2, symptoms="b", urgencyLevel=2, queuePosition=2, arrivalTime=base_time, urgency="2"),
        ]
        result = service.get_sorted_queue()
        assert result[0].id == 2  # earlier time first
        assert result[1].id == 1  # later time second

    def test_reorder_queue_assigns_correct_positions(self, service, mock_repo):
        base_time = datetime.now(timezone.utc)
        patients = [
            PatientResponse(id=1, symptoms="a", urgencyLevel=3, queuePosition=5, arrivalTime=base_time, urgency="3"),
            PatientResponse(id=2, symptoms="b", urgencyLevel=1, queuePosition=3, arrivalTime=base_time + timedelta(minutes=1), urgency="1"),
            PatientResponse(id=3, symptoms="c", urgencyLevel=2, queuePosition=9, arrivalTime=base_time + timedelta(minutes=2), urgency="2"),
        ]
        mock_repo.get_all.return_value = patients
        mock_repo.update.return_value = patients[0]
        service.reorder_queue()
        # Should have called update for each patient with new queuePosition
        assert mock_repo.update.call_count == 3
        calls = mock_repo.update.call_args_list
        # For patient 2 (urgency 1): position 0
        assert calls[0][0][1].queuePosition == 0
        # For patient 3 (urgency 2): position 1
        assert calls[1][0][1].queuePosition == 1
        # For patient 1 (urgency 3): position 2
        assert calls[2][0][1].queuePosition == 2

    def test_take_next_patient_returns_most_urgent(self, service, mock_repo):
        base_time = datetime.now(timezone.utc)
        mock_repo.get_all.side_effect = [
            [  # First call for get_sorted_queue
                PatientResponse(id=1, symptoms="a", urgencyLevel=3, queuePosition=0, arrivalTime=base_time, urgency="3"),
                PatientResponse(id=2, symptoms="b", urgencyLevel=1, queuePosition=1, arrivalTime=base_time + timedelta(minutes=1), urgency="1"),
            ],
            [  # Second call after delete (reorder_queue)
                PatientResponse(id=2, symptoms="b", urgencyLevel=1, queuePosition=0, arrivalTime=base_time + timedelta(minutes=1), urgency="1"),
            ],
        ]
        mock_repo.delete.return_value = True
        result = service.take_next_patient()
        assert result.id == 2  # most urgent (urgency 1)
        mock_repo.delete.assert_called_once_with(2)

    def test_take_next_patient_empty_queue_raises(self, service, mock_repo):
        mock_repo.get_all.return_value = []
        with pytest.raises(IndexError, match="No patients"):
            service.take_next_patient()
