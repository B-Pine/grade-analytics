"""Rank students by average score, handling ties."""

from collections.abc import Sequence

from ..models import RankingEntry, Student
from .aggregators import rank_by_average
from .stats import percentile_rank


def rank_students(students: Sequence[Student]) -> list[RankingEntry]:
    """Rank students by average, best first, using competition ranking.

    Students with the same average (to 2 decimals) share a rank, and the
    next rank skips accordingly: 1, 2, 2, 4. Students without grades are
    left out.

    Args:
        students: Students to rank. A Sequence because it is read twice.

    Returns:
        One RankingEntry per graded student, in rank order.
    """
    by_id = {
        student.student_id: student 
        for student in students
    }
    ordered = rank_by_average(students)
    averages = list(ordered.values())

    entries: list[RankingEntry] = []
    rank = 0
    previous: float | None = None

    for position, (student_id, average) in enumerate(ordered.items(), start=1):
        rounded = round(average, 2)
        if rounded != previous:
            rank, previous = position, rounded
        entries.append(
            RankingEntry(rank, by_id[student_id], average, percentile_rank(average, averages))
        )
    return entries