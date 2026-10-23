"""RankingEntry model."""

from typing import NamedTuple

from .student import Student

# here I use NamedTuple because ranking entry is a small and read-only result.
class RankingEntry(NamedTuple):
    """One student's position in a ranking.

    Attributes:
        rank: Position in the ranking. Tied students share a rank.
        student: The ranked student.
        average: The student's average score.
        percentile: Percentile rank of the average among all ranked students.
    """

    rank: int
    student: Student
    average: float
    percentile: float
