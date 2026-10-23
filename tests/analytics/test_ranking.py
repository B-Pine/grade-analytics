"""Tests for the tie-aware ranking."""

from grade_analytics.analytics import rank_students
from grade_analytics.models import Course, Grade, RankingEntry, Student


def make_students(course: Course, averages: list[float]) -> list[Student]:
    """One student per average, named A, B, C..."""
    return [
        Student(f"S{i}", chr(65 + i), "CS", 1, [Grade(course, "2025-S1", avg)])
        for i, avg in enumerate(averages)
    ]


def test_ties_share_a_rank_and_the_next_rank_skips(course: Course) -> None:
    ranking = rank_students(make_students(course, [90, 85, 85, 70]))
    assert [(e.rank, e.student.name) for e in ranking] == [
        (1, "A"), (2, "B"), (2, "C"), (4, "D"),
    ]


def test_nearly_equal_averages_count_as_a_tie(course: Course) -> None:
    ranking = rank_students(make_students(course, [85.0, 85.000000001]))
    assert [e.rank for e in ranking] == [1, 1]


def test_students_without_grades_are_not_ranked(students: list[Student]) -> None:
    assert [e.student.name for e in rank_students(students)] == ["Aline", "Eric"]


def test_percentiles_use_mid_rank(course: Course) -> None:
    ranking = rank_students(make_students(course, [90, 80, 70, 60]))
    assert [e.percentile for e in ranking] == [87.5, 62.5, 37.5, 12.5]


def test_entries_are_named_tuples(students: list[Student]) -> None:
    entry = rank_students(students)[0]
    assert isinstance(entry, RankingEntry)
    rank, student, average, percentile = entry
    assert (rank, student.name, average, percentile) == (1, "Aline", 85.0, 75.0)