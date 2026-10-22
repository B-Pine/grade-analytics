"""TypedDict definitions describing the JSON report structure."""

from typing import Optional, TypedDict


class RankedStudent(TypedDict):
    """One entry in the top performers list."""

    rank: int
    student_id: str
    name: str
    average: float


class MajorSummary(TypedDict):
    """Aggregated figures for one major."""

    student_count: int
    average: Optional[float]


class SummaryReport(TypedDict):
    """The complete summary report written to JSON."""

    generated_at: str
    source_file: str
    total_students: int
    total_grades: int
    grade_distribution: dict[str, int]
    majors: dict[str, MajorSummary]
    top_performers: list[RankedStudent]
