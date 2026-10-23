"""Tests for the Grade model."""

import dataclasses

import pytest

from grade_analytics.exceptions import GradeAnalyticsError, InvalidScoreError
from grade_analytics.models import Course, Grade


@pytest.mark.parametrize(
    ("score", "letter"),
    [
        (100, "A"), (90, "A"),
        (89.99, "B"), (80, "B"),
        (79.99, "C"), (70, "C"),
        (69.99, "D"), (60, "D"),
        (59.99, "F"), (0, "F"),
    ],
)
def test_letter_grade_boundaries(course: Course, score: float, letter: str) -> None:
    assert Grade(course, "2025-S1", score).letter == letter


@pytest.mark.parametrize("score", [0, 100])
def test_accepts_range_limits(course: Course, score: float) -> None:
    assert Grade(course, "2025-S1", score).score == score


@pytest.mark.parametrize("score", [-0.1, 100.1, -50, 150])
def test_rejects_scores_outside_range(course: Course, score: float) -> None:
    with pytest.raises(InvalidScoreError, match="0 - 100"):
        Grade(course, "2025-S1", score)


def test_invalid_score_is_a_package_error(course: Course) -> None:
    with pytest.raises(GradeAnalyticsError):
        Grade(course, "2025-S1", 101)


def test_is_immutable(course: Course) -> None:
    grade = Grade(course, "2025-S1", 80)
    with pytest.raises(dataclasses.FrozenInstanceError):
        grade.score = 100  # type: ignore[misc]