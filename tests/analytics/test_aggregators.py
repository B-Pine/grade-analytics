"""Tests for the collection-based aggregators.

Grouped by collection type, as the brief asks for tests per collection.
"""

from collections import Counter, OrderedDict

import pytest

from grade_analytics.analytics import (
    grade_distribution,
    group_by_major,
    group_by_year,
    rank_by_average,
    rolling_average,
    student_trend,
)
from grade_analytics.models import Course, Grade, Student


# Test Counter

def test_grade_distribution_counts_letters(students: list[Student]) -> None:
    distribution = grade_distribution(students)
    assert isinstance(distribution, Counter)
    assert distribution == {"A": 1, "C": 1, "D": 1}


def test_grade_distribution_missing_letter_counts_as_zero(students: list[Student]) -> None:
    assert grade_distribution(students)["F"] == 0


def test_grade_distribution_accepts_a_generator(students: list[Student]) -> None:
    assert grade_distribution(s for s in students) == {"A": 1, "C": 1, "D": 1}


# test defaultdict

def test_group_by_major(students: list[Student]) -> None:
    groups = group_by_major(students)
    assert [s.name for s in groups["CS"]] == ["Aline", "Grace"]
    assert [s.name for s in groups["Econ"]] == ["Eric"]


def test_group_by_major_unknown_key_returns_empty_list(students: list[Student]) -> None:
    assert group_by_major(students)["Physics"] == []


def test_group_by_year(students: list[Student]) -> None:
    groups = group_by_year(students)
    assert [s.name for s in groups[1]] == ["Eric", "Grace"]
    assert [s.name for s in groups[2]] == ["Aline"]


# test OrderedDict

def test_rank_by_average_orders_best_first(students: list[Student]) -> None:
    ranking = rank_by_average(students)
    assert isinstance(ranking, OrderedDict)
    assert list(ranking.items()) == [("S001", 85.0), ("S002", 65.0)]


def test_rank_by_average_skips_students_without_grades(students: list[Student]) -> None:
    assert "S003" not in rank_by_average(students)


# test deque usage

def test_rolling_average_slides_the_window() -> None:
    assert rolling_average([80, 90, 70, 100], window=3) == [80.0, 85.0, 80.0, 86.67]


def test_rolling_average_window_of_one_returns_the_scores() -> None:
    assert rolling_average([70, 80, 90], window=1) == [70.0, 80.0, 90.0]


def test_rolling_average_window_larger_than_data() -> None:
    assert rolling_average([60, 80], window=10) == [60.0, 70.0]


def test_rolling_average_of_nothing_is_empty() -> None:
    assert rolling_average([], window=3) == []


@pytest.mark.parametrize("window", [0, -1])
def test_rolling_average_rejects_invalid_window(window: int) -> None:
    with pytest.raises(ValueError, match="window"):
        rolling_average([80, 90], window=window)


def test_student_trend_sorts_by_semester(course: Course) -> None:
    student = Student("S1", "Aline", "CS", 2, [
        Grade(course, "2025-S1", 60),
        Grade(course, "2024-S1", 90),   # earliest, listed second on purpose
    ])
    assert student_trend(student) == [90.0, 75.0]