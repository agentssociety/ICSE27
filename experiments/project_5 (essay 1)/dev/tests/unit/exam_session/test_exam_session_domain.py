from __future__ import annotations

import pytest
from src.domain.exam_session import ExamSession, Exam


class TestExamSessionDomain:
    def test_create_exam_session(self) -> None:
        session = ExamSession(student_id="student1", exam_id="exam1")
        assert session.student_id == "student1"
        assert session.exam_id == "exam1"
        assert session.status == "in_progress"

    def test_record_answer(self) -> None:
        session = ExamSession(student_id="student1", exam_id="exam1")
        session.record_answer("q1", "answer1")
        assert session.answers == {"q1": "answer1"}

    def test_end_exam(self) -> None:
        session = ExamSession(student_id="student1", exam_id="exam1")
        session.end_exam()
        assert session.status == "completed"
