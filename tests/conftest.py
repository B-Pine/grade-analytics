"""Shared fixtures for the whole test suite.

pytest finds this file automatically: every fixture defined here can be
used by any test, just by naming it as a parameter.
"""

import csv
from collections.abc import Callable
from pathlib import Path

import pytest

from grade_analytics.models import Course, Grade, Student

HEADER = [
    "student_id", "name", "major", "year",
    "course_code", "course_name", "credits", "semester", "score",
]


@pytest.fixture
def course() -> Course:
    """A single course to build grades with."""
    return Course("CS201", "Data Structures", 4)


@pytest.fixture
def students(course: Course) -> list[Student]:
    """Three students: two with grades, one without.

    Aline: 92, 78 (average 85.0) | Eric: 65 | Grace: no grades
    """
    return [
        Student("S001", "Aline", "CS", 2,
                [Grade(course, "2025-S1", 92), Grade(course, "2025-S2", 78)]),
        Student("S002", "Eric", "Econ", 1, [Grade(course, "2025-S1", 65)]),
        Student("S003", "Grace", "CS", 1),
    ]


@pytest.fixture
def valid_row() -> list[str]:
    """One correct CSV data row. Tests copy it and break one value."""
    return ["S001", "Aline Uwase", "Computer Science", "2",
            "CS201", "Data Structures", "4", "2025-S1", "87.5"]


@pytest.fixture
def write_csv(tmp_path: Path) -> Callable[..., Path]:
    """Factory that writes a CSV into a temporary folder and returns its path.

    tmp_path is a built-in pytest fixture: a fresh, empty folder per test
    that pytest cleans up afterwards, so tests never touch real files.
    """
    def _write(rows: list[list[str]], header: list[str] = HEADER,
               name: str = "grades.csv") -> Path:
        path = tmp_path / name
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        return path

    return _write