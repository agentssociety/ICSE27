from __future__ import annotations

import pytest
from src.domain.cohort import Cohort


class TestCohortDomain:
    def test_create_cohort(self) -> None:
        cohort = Cohort(name="Math Class")
        assert cohort.name == "Math Class"
        assert cohort.get_student_count() == 0

    def test_add_student(self) -> None:
        cohort = Cohort(name="Math Class")
        cohort.add_student("student1")
        assert cohort.get_student_count() == 1

    def test_remove_student(self) -> None:
        cohort = Cohort(name="Math Class")
        cohort.add_student("student1")
        cohort.remove_student("student1")
        assert cohort.get_student_count() == 0
