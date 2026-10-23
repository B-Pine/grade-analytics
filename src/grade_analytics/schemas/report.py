"""TypedDict definitions describing the JSON report structure."""

from typing import Optional, TypedDict


class ScoreStatistics(TypedDict):
    """Descriptive statistics for a set of scores."""

    count: int
    mean: float
    median: float
    mode: list[float]
    min: float
    max: float


class RankedStudent(TypedDict):
    """One entry in the top performers list."""

    rank: int
    student_id: str
    name: str
    major: str
    average: float
    percentile: float
    trend: list[float]


class MajorSummary(TypedDict):
    """Aggregated figures for one major."""

    student_count: int
    statistics: Optional[ScoreStatistics]


class SummaryReport(TypedDict):
    """The complete summary report written to JSON."""

    generated_at: str
    source_file: str
    total_students: int
    overall_statistics: Optional[ScoreStatistics]
    grade_distribution: dict[str, int]
    majors: dict[str, MajorSummary]
    top_performers: list[RankedStudent]
