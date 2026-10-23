"""Assemble a SummaryReport from loaded students."""

from collections.abc import Sequence
from datetime import datetime, timezone
from itertools import islice
from pathlib import Path
from typing import Optional

from ..analytics import (
    grade_distribution,
    group_by_major,
    mean,
    median,
    mode,
    rank_students,
    student_trend,
)
from ..models import Student
from ..schemas import MajorSummary, RankedStudent, ScoreStatistics, SummaryReport

LETTERS = ("A", "B", "C", "D", "F")


def build_summary(
    students: Sequence[Student], source: Path | str, top_n: int = 5
) -> SummaryReport:
    """Build the summary report for a set of students.

    Args:
        students: Loaded students. A Sequence because it is read several times.
        source: The CSV the students came from, recorded in the report.
        top_n: How many top performers to include.

    Returns:
        A SummaryReport ready to be written with write_report().
    """
    distribution = grade_distribution(students)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_file": Path(source).name,
        "total_students": len(students),
        "overall_statistics": _describe(_scores_of(students)),
        "grade_distribution": {letter: distribution[letter] for letter in LETTERS},
        "majors": _summarize_majors(students),
        "top_performers": _top_performers(students, top_n),
    }


def _scores_of(students: Sequence[Student]) -> list[float]:
    """Every score of every given student, flattened into one list."""
    return [
        grade.score 
        for student in students 
        for grade in student.grades
    ]


def _describe(scores: Sequence[float]) -> Optional[ScoreStatistics]:
    """Rounded descriptive statistics, or None if there are no scores."""
    if not scores:
        return None
    return {
        "count": len(scores),
        "mean": round(mean(scores), 2),
        "median": round(median(scores), 2),
        "mode": mode(scores),
        "min": min(scores),
        "max": max(scores),
    }


def _summarize_majors(students: Sequence[Student]) -> dict[str, MajorSummary]:
    """Student count and score statistics per major, sorted by major name."""
    return {
        major: {"student_count": len(group), "statistics": _describe(_scores_of(group))}
        for major, group in sorted(group_by_major(students).items())
    }


def _top_performers(students: Sequence[Student], top_n: int) -> list[RankedStudent]:
    """The first top_n entries of the tie-aware ranking."""
    return [
        {
            "rank": entry.rank,
            "student_id": entry.student.student_id,
            "name": entry.student.name,
            "major": entry.student.major,
            "average": round(entry.average, 2),
            "percentile": round(entry.percentile, 2),
            "trend": student_trend(entry.student),
        }
        for entry in islice(rank_students(students), top_n)
    ]