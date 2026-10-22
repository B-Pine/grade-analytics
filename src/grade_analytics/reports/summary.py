"""Assemble a SummaryReport from loaded students."""

from collections.abc import Sequence
from datetime import datetime, timezone
from itertools import islice
from pathlib import Path

from grade_analytics.analytics import grade_distribution, group_by_major, rank_by_average
from grade_analytics.models import Student
from grade_analytics.schemas import MajorSummary, RankedStudent, SummaryReport

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
        "total_grades": sum(len(student.grades) for student in students),
        "grade_distribution": {letter: distribution[letter] for letter in LETTERS},
        "majors": _summarize_majors(students),
        "top_performers": _top_performers(students, top_n),
    }


def _summarize_majors(students: Sequence[Student]) -> dict[str, MajorSummary]:
    """Student count and average score per major, sorted by major name."""
    summaries: dict[str, MajorSummary] = {}
    
    for major, group in sorted(group_by_major(students).items()):
        scores = [grade.score for student in group for grade in student.grades]
        summaries[major] = {
            "student_count": len(group),
            "average": round(sum(scores) / len(scores), 2) if scores else None,
        }
    return summaries


def _top_performers(students: Sequence[Student], top_n: int) -> list[RankedStudent]:
    """The top_n students by average, using the OrderedDict ranking."""
    names = {student.student_id: student.name for student in students}
    ranking = rank_by_average(students)
    return [
        {"rank": rank, "student_id": student_id, "name": names[student_id], "average": round(avg, 2)}
        for rank, (student_id, avg) in enumerate(islice(ranking.items(), top_n), start=1)
    ]