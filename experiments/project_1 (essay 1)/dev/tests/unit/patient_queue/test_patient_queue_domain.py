from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.patient_queue import PatientQueue, QueueState
from src.domain.patient import Patient, RecordState


def test_sort_by_urgency_and_arrival_orders_highest_urgency_first() -> None:
    """Given patients with different urgency levels, sorting puts highest urgency first."""
    queue = PatientQueue(queueId=uuid4())
    now = datetime.now()

    p1 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=0)
    p2 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=1)
    p3 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=2)

    queue.patients = [p3, p1, p2]
    sorted_patients = queue.sortByUrgencyAndArrival()

    assert sorted_patients[0].urgency_level == 0
    assert sorted_patients[1].urgency_level == 1
    assert sorted_patients[2].urgency_level == 2


def test_sort_by_urgency_and_arrival_same_urgency_earliest_first() -> None:
    """Given patients with same urgency, sorting puts earliest arrival first."""
    queue = PatientQueue(queueId=uuid4())
    now = datetime.now()

    p1 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=1)
    p2 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=10), urgency_level=1)
    p3 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=5), urgency_level=1)

    queue.patients = [p1, p2, p3]
    sorted_patients = queue.sortByUrgencyAndArrival()

    assert sorted_patients[0].patientId == p1.patientId  # earliest
    assert sorted_patients[1].patientId == p3.patientId  # second
    assert sorted_patients[2].patientId == p2.patientId  # latest


def test_sort_by_urgency_and_arrival_mixed() -> None:
    """Given mixed urgency and arrival times, sorting respects both criteria."""
    queue = PatientQueue(queueId=uuid4())
    now = datetime.now()

    # p1: urgency 0 (critical), earliest
    # p2: urgency 0 (critical), later
    # p3: urgency 1 (high), earliest
    # p4: urgency 1 (high), later
    p1 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=0)
    p2 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=5), urgency_level=0)
    p3 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now, urgency_level=1)
    p4 = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE, arrival_time=now + timedelta(seconds=5), urgency_level=1)

    queue.patients = [p4, p2, p3, p1]
    sorted_patients = queue.sortByUrgencyAndArrival()

    assert sorted_patients[0].patientId == p1.patientId  # critical, earliest
    assert sorted_patients[1].patientId == p2.patientId  # critical, later
    assert sorted_patients[2].patientId == p3.patientId  # high, earliest
    assert sorted_patients[3].patientId == p4.patientId  # high, later


def test_update_order_changes_state_to_post_sort() -> None:
    """After updateOrder, state becomes POST_SORT."""
    queue = PatientQueue(queueId=uuid4())
    assert queue.state == QueueState.PRE_SORT
    queue.updateOrder([])
    assert queue.state == QueueState.POST_SORT


def test_read_all_returns_copy() -> None:
    """readAllPatients returns a copy of the patients list."""
    queue = PatientQueue(queueId=uuid4())
    p = Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE)
    queue.patients = [p]
    result = queue.readAllPatients()
    assert result == [p]
    result.append(Patient(patientId=uuid4(), state=RecordState.PENDING_TRIAGE))
    assert len(queue.patients) == 1  # original unchanged
