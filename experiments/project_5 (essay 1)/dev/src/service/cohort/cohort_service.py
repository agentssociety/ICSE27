from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.cohort import Cohort
    from src.domain.student import Student
    from src.repository.cohort import CohortRepository

"""
Service layer for the Cohort domain class

Package: service.cohort
Layer: service
Related tasks: #108, #115
Requirement coverage:
- Cohort Creation and Management
- Cohort Leaderboard Ranked by Nuggets
"""

class CohortService(Protocol):
    ...

class CohortServiceImpl:
    def __init__(self, cohortRepository: CohortRepository | None = None, abstract_createCohort_name: str | None = None, abstract_enrollStudent_cohort: Cohort | None = None, abstract_deleteCohort_cohort: Cohort | None = None, abstract_getCohort_name: str | None = None) -> None:
        self.cohortRepository = cohortRepository
        self.abstract_createCohort_name = abstract_createCohort_name
        self.abstract_enrollStudent_cohort = abstract_enrollStudent_cohort
        self.abstract_deleteCohort_cohort = abstract_deleteCohort_cohort
        self.abstract_getCohort_name = abstract_getCohort_name