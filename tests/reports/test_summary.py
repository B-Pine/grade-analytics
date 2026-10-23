"""Tests for building the summary report."""

import json

from grade_analytics.models import Student
from grade_analytics.reports import build_summary
from grade_analytics.schemas import SummaryReport


def test_report_has_exactly_the_schema_keys(students: list[Student]) -> None:
    report = build_summary(students, "data/grades.csv")
    assert set(report) == set(SummaryReport.__annotations__)


def test_source_is_recorded_as_file_name(students: list[Student]) -> None:
    assert build_summary(students, "data/grades.csv")["source_file"] == "grades.csv"


def test_distribution_lists_every_letter_in_order(students: list[Student]) -> None:
    distribution = build_summary(students, "x.csv")["grade_distribution"]
    assert distribution == {"A": 1, "B": 0, "C": 1, "D": 1, "F": 0}
    assert list(distribution) == ["A", "B", "C", "D", "F"]


def test_overall_statistics(students: list[Student]) -> None:
    assert build_summary(students, "x.csv")["overall_statistics"] == {
        "count": 3, "mean": 78.33, "median": 78.0, "mode": [], "min": 65, "max": 92,
    }


def test_major_without_grades_has_no_statistics(students: list[Student]) -> None:
    students.append(Student("S004", "Yves", "Physics", 1))
    majors = build_summary(students, "x.csv")["majors"]
    assert list(majors) == ["CS", "Econ", "Physics"]
    assert majors["Physics"] == {"student_count": 1, "statistics": None}


def test_top_performers_respects_top_n(students: list[Student]) -> None:
    top = build_summary(students, "x.csv", top_n=1)["top_performers"]
    assert [entry["name"] for entry in top] == ["Aline"]
    assert top[0]["trend"] == [92.0, 85.0]


def test_empty_input_gives_an_empty_report() -> None:
    report = build_summary([], "x.csv")
    assert report["total_students"] == 0
    assert report["overall_statistics"] is None
    assert report["top_performers"] == []


def test_report_is_json_serializable(students: list[Student]) -> None:
    json.dumps(build_summary(students, "x.csv"))