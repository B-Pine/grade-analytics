"""Computations over student data: aggregations and statistics."""

from .aggregators import (
    grade_distribution,
    group_by_major,
    group_by_year,
    rank_by_average,
    rolling_average,
    student_trend,
)

__all__ = [
    "grade_distribution",
    "group_by_major",
    "group_by_year",
    "rank_by_average",
    "rolling_average",
    "student_trend",
]
