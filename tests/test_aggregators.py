"""Remove the @pytest.mark.skip line when you start implementing a function."""
import pytest

from grade_analytics.aggregators import (
    grade_distribution,
    group_by_major,
    rank_by_average,
    rolling_average,
)
from grade_analytics.models import Student


def test_grade_distribution(students: list[Student]) -> None:
    assert grade_distribution(students) == {"A": 1, "C": 1, "D": 1}


@pytest.mark.skip(reason="TODO: implement group_by_major")
def test_group_by_major(students: list[Student]) -> None:
    groups = group_by_major(students)
    assert [s.name for s in groups["CS"]] == ["Aline", "Grace"]
    assert groups["Physics"] == []  # defaultdict never raises KeyError


@pytest.mark.skip(reason="TODO: implement rank_by_average")
def test_rank_by_average(students: list[Student]) -> None:
    ranking = rank_by_average(students)
    assert list(ranking) == ["Aline", "Eric"]  # Grace has no grades
    assert ranking["Aline"] == 85.0


@pytest.mark.skip(reason="TODO: implement rolling_average")
def test_rolling_average() -> None:
    result = rolling_average([80, 90, 70, 100], window=3)
    assert result == pytest.approx([80.0, 85.0, 80.0, 86.67], abs=0.01)
