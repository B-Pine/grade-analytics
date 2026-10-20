import dataclasses

import pytest

from grade_analytics.models import Course, Grade, Student


def test_score_out_of_range_is_rejected(cs201: Course) -> None:
    with pytest.raises(ValueError):
        Grade(cs201, "2025-S1", 101)


@pytest.mark.parametrize(
    "score, letter",
    [(95, "A"), (90, "A"), (85, "B"), (72, "C"), (60, "D"), (59.9, "F")],
)
def test_letter_grade(cs201: Course, score: float, letter: str) -> None:
    assert Grade(cs201, "2025-S1", score).letter == letter


def test_grade_is_immutable(cs201: Course) -> None:
    grade = Grade(cs201, "2025-S1", 80)
    with pytest.raises(dataclasses.FrozenInstanceError):
        grade.score = 100  # type: ignore[misc]


def test_average_without_grades_is_none() -> None:
    assert Student("S9", "Nobody", "CS", 1).average() is None


def test_students_do_not_share_grade_lists() -> None:
    a = Student("S1", "A", "CS", 1)
    b = Student("S2", "B", "CS", 1)
    assert a.grades is not b.grades
