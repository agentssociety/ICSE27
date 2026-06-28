from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from src.dto.triage.triage_dto import (
    TriageAssessmentCreate,
    TriageAssessmentResponse,
    TriageQueueEntry,
)
from src.orm.patient.patient_orm import PatientORM
from src.orm.triage.triage_orm import TriageAssessmentORM


class SQLAlchemyTriageRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def assess(self, data: TriageAssessmentCreate) -> TriageAssessmentResponse:
        now = datetime.now(timezone.utc).isoformat()
        row = TriageAssessmentORM(
            id=str(uuid.uuid4()),
            patientId=data.patientId,
            severity=data.severity,
            notes=data.notes,
            createdAt=now,
            inQueue=True,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TriageAssessmentResponse.model_validate(row)

    def get_queue(self) -> list[TriageQueueEntry]:
        rows = (
            self._session.query(TriageAssessmentORM)
            .filter(TriageAssessmentORM.inQueue == True)  # noqa: E712
            .all()
        )
        now = datetime.now(timezone.utc)
        entries: list[TriageQueueEntry] = []
        for row in rows:
            patient = self._session.get(PatientORM, row.patientId)
            patient_name = (
                f"{patient.firstName} {patient.lastName}" if patient else "Unknown"
            )
            assessed_at = datetime.fromisoformat(row.createdAt)
            if assessed_at.tzinfo is None:
                assessed_at = assessed_at.replace(tzinfo=timezone.utc)
            wait_minutes = max(0, int((now - assessed_at).total_seconds() / 60))
            entries.append(
                TriageQueueEntry(
                    patientId=row.patientId,
                    patientName=patient_name,
                    severity=row.severity,
                    waitTimeMinutes=wait_minutes,
                    assessedAt=row.createdAt,
                )
            )
        return entries

    def remove_from_queue(self, patient_id: str) -> bool:
        row = (
            self._session.query(TriageAssessmentORM)
            .filter(
                TriageAssessmentORM.patientId == patient_id,
                TriageAssessmentORM.inQueue == True,  # noqa: E712
            )
            .first()
        )
        if row is None:
            return False
        row.inQueue = False
        self._session.commit()
        return True

    def get_queue_stats(self) -> dict:
        rows = (
            self._session.query(TriageAssessmentORM)
            .filter(TriageAssessmentORM.inQueue == True)  # noqa: E712
            .all()
        )
        if not rows:
            return {"count": 0, "avg_wait": 0.0, "severity_breakdown": {}}
        now = datetime.now(timezone.utc)
        wait_times: list[float] = []
        severity_breakdown: dict[str, int] = {}
        for row in rows:
            assessed_at = datetime.fromisoformat(row.createdAt)
            if assessed_at.tzinfo is None:
                assessed_at = assessed_at.replace(tzinfo=timezone.utc)
            wait_times.append((now - assessed_at).total_seconds() / 60)
            key = str(row.severity)
            severity_breakdown[key] = severity_breakdown.get(key, 0) + 1
        return {
            "count": len(rows),
            "avg_wait": sum(wait_times) / len(wait_times),
            "severity_breakdown": severity_breakdown,
        }
