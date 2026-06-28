from __future__ import annotations

from typing import Any, Protocol

"""
Repository layer for the UrgencyLevel domain class

Package: repository.urgency_level
Layer: repository
Related tasks: #2, #3, #4, #6
Requirement coverage:
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Real-time Patient Dashboard
"""

class TriageNurseInterface(Protocol):
    ...

class PatientInformationDatabase(Protocol):
    ...
