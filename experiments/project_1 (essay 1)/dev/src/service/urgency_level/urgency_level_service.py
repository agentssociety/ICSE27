from __future__ import annotations

from typing import Any, Protocol

from src.domain.urgency_level import UrgencyLevel, urgency_to_int
from src.domain.patient import Patient

"""
Service layer for the UrgencyLevel domain class

Package: service.urgency_level
Layer: service
Related tasks: #2, #3, #4, #6
Requirement coverage:
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Real-time Patient Dashboard
"""


class UrgencyLevelService(Protocol):
    def assign_urgency(self, patient: Patient, symptoms: list[str]) -> UrgencyLevel:
        """Assign an urgency level to a patient based on their symptoms."""
        ...

    def get_urgency_sort_value(self, level: UrgencyLevel) -> int:
        """Get the numeric sort value for an urgency level (lower = more urgent)."""
        ...


class UrgencyLevelServiceImpl:
    def __init__(self) -> None:
        pass

    def assign_urgency(self, patient: Patient, symptoms: list[str]) -> UrgencyLevel:
        """Assign an urgency level to a patient based on their symptoms.
        
        Simple heuristic: if any symptom suggests critical condition, assign CRITICAL.
        Otherwise HIGH, MEDIUM, or LOW based on symptom severity keywords.
        """
        critical_keywords = {"cardiac arrest", "stroke", "severe bleeding", "unconscious", "not breathing"}
        high_keywords = {"chest pain", "difficulty breathing", "severe pain", "high fever", "fracture"}
        medium_keywords = {"moderate pain", "nausea", "dizziness", "mild fever", "cut", "burn"}

        symptom_set = {s.lower() for s in symptoms}

        if symptom_set & critical_keywords:
            return UrgencyLevel.CRITICAL
        if symptom_set & high_keywords:
            return UrgencyLevel.HIGH
        if symptom_set & medium_keywords:
            return UrgencyLevel.MEDIUM
        return UrgencyLevel.LOW

    def get_urgency_sort_value(self, level: UrgencyLevel) -> int:
        """Get the numeric sort value for an urgency level (lower = more urgent)."""
        return urgency_to_int(level.value)
