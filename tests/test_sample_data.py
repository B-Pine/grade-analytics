"""Checks that the committed sample dataset meets the lab requirements."""

from pathlib import Path

import pytest

from grade_analytics.file_io import load_students
from grade_analytics.models import Student

SAMPLE = Path(__file__).parents[1] / "data" / "students.csv"


@pytest.fixture(scope="module")
def sample_students() -> list[Student]:
    """Loaded once for all tests in this file, since it never changes."""
    return load_students(SAMPLE)


def test_has_at_least_50_students(sample_students: list[Student]) -> None:
    assert len(sample_students) >= 50


def test_every_student_has_grades(sample_students: list[Student]) -> None:
    assert all(student.grades for student in sample_students)


def test_covers_several_majors_and_semesters(sample_students: list[Student]) -> None:
    majors = {student.major for student in sample_students}
    semesters = {g.semester for student in sample_students for g in student.grades}
    assert len(majors) >= 3
    assert len(semesters) >= 3