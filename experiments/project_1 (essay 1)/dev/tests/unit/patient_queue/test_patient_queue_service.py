from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.patient_queue import PatientQueue, QueueState
from src.domain.patient import Patient, RecordState
from src.service.patient_queue.patient_queue_service import PatientQueueServiceImpl


@pytest.fixture
def service() -> PatientQueueServiceImpl:
    return PatientQueueServiceImpl()


@pytest.fixture
def queue() -> PatientQueue:
    return PatientQueue(queueId=uuid4())


@pytest.fixture
def patients() -> list[Patient]:
    now = datetime.now()
    return [
        Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=2),
        Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=5), urgency_level=0),
        Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=10), urgency_level=1),
    ]


def test_sort_queue_orders_by_urgency_then_arrival(service: PatientQueueServiceImpl, queue: PatientQueue, patients: list[Patient]) -> None:
    """sort_queue returns patients sorted by urgency (highest first) then arrival time."""
    queue.patients = patients
    sorted_patients = service.sort_queue(queue)

    # urgency 0 first, then 1, then 2
    assert sorted_patients[0].urgency_level == 0
    assert sorted_patients[1].urgency_level == 1
    assert sorted_patients[2].urgency_level == 2


def test_sort_queue_updates_state(service: PatientQueueServiceImpl, queue: PatientQueue, patients: list[Patient]) -> None:
    """After sort_queue, queue state is POST_SORT."""
    queue.patients = patients
    assert queue.state == QueueState.PRE_SORT
    service.sort_queue(queue)
    assert queue.state == QueueState.POST_SORT


def test_get_next_patient_returns_highest_priority(service: PatientQueueServiceImpl, queue: PatientQueue, patients: list[Patient]) -> None:
    """get_next_patient returns the patient with highest urgency (lowest urgency_level)."""
    queue.patients = patients
    next_patient = service.get_next_patient(queue)
    assert next_patient is not None
    assert next_patient.urgency_level == 0


def test_get_next_patient_empty_queue(service: PatientQueueServiceImpl, queue: PatientQueue) -> None:
    """get_next_patient returns None for empty queue."""
    assert service.get_next_patient(queue) is None


def test_dequeue_next_removes_and_returns_highest_priority(service: PatientQueueServiceImpl, queue: PatientQueue, patients: list[Patient]) -> None:
    """dequeue_next removes and returns the highest priority patient."""
    queue.patients = patients
    next_patient = service.dequeue_next(queue)
    assert next_patient is not None
    assert next_patient.urgency_level == 0
    assert len(queue.patients) == 2


def test_dequeue_next_empty_queue(service: PatientQueueServiceImpl, queue: PatientQueue) -> None:
    """dequeue_next returns None for empty queue."""
    assert service.dequeue_next(queue) is None
