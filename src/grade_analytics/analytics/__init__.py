"""Computations over student data: aggregations, statistics and rankings."""

from .aggregators import (
    grade_distribution,
    group_by_major,
    group_by_year,
    rank_by_average,
    rolling_average,
    student_trend,
)
from .ranking import rank_students
from .stats import mean, median, mode, percentile_rank

__all__ = [
    "grade_distribution",
    "group_by_major",
    "group_by_year",
    "rank_by_average",
    "rolling_average",
    "student_trend",
    "rank_students",
    "mean",
    "median",
    "mode",
    "percentile_rank",
]