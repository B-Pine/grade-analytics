"""Collection-based aggregators for student data.

Each function uses the collections type best suited to its job.
"""

from collections import Counter, OrderedDict, defaultdict, deque
from collections.abc import Iterable

from ..models import Student


def grade_distribution(students: Iterable[Student]) -> Counter[str]:
    """Count letter grades across all students and courses.

    Args:
        students: Students whose grades should be counted.

    Returns:
        A Counter mapping each letter grade to how often it occurs.
        Use ``.most_common(n)`` to get the n most frequent grades.
    """
    return Counter(grade.letter for student in students for grade in student.grades)


def group_by_major(students: Iterable[Student]) -> defaultdict[str, list[Student]]:
    """Group students by their major.

    Args:
        students: Students to group.

    Returns:
        A defaultdict mapping each major to its students. Looking up a
        major with no students returns an empty list instead of raising
        KeyError.
    """
    groups: defaultdict[str, list[Student]] = defaultdict(list)
    for student in students:
        groups[student.major].append(student)
    return groups


def group_by_year(students: Iterable[Student]) -> defaultdict[int, list[Student]]:
    """Group students by their year of study.

    Args:
        students: Students to group.

    Returns:
        A defaultdict mapping each year to its students.
    """
    groups: defaultdict[int, list[Student]] = defaultdict(list)
    for student in students:
        groups[student.year].append(student)
    return groups


def rank_by_average(students: Iterable[Student]) -> OrderedDict[str, float]:
    """Rank students by average score, highest first.

    Students without grades are left out, since they have no average.

    Args:
        students: Students to rank.

    Returns:
        An OrderedDict mapping student_id to average score, in rank order.
        Keyed by ID rather than name because two students can share a name.
    """
    averages = [
        (student.student_id, avg)
        for student in students
        if (avg := student.average()) is not None   # walrus operation -> avg=student.average(); if avg is not None:
    ]
    averages.sort(key=lambda pair: pair[1], reverse=True)
    return OrderedDict(averages)


def rolling_average(scores: Iterable[float], window: int = 3) -> list[float]:
    """Compute a rolling average over a sequence of scores.

    A deque with ``maxlen=window`` automatically drops the oldest score
    when a new one arrives, so it always holds the current window.

    Args:
        scores: Scores in chronological order.
        window: Number of most recent scores to average. Must be at least 1.

    Returns:
        One average per score, rounded to 2 decimals. Until the window
        fills up, each average uses the scores seen so far.

    Raises:
        ValueError: If window is less than 1.

    Example:
        >>> rolling_average([80, 90, 70, 100], window=3)
        [80.0, 85.0, 80.0, 86.67]
    """
    if window < 1:
        raise ValueError(f"window must be at least 1, got {window}")

    recent: deque[float] = deque(maxlen=window)
    averages: list[float] = []
    for score in scores:
        recent.append(score)
        averages.append(round(sum(recent) / len(recent), 2))
    return averages


def student_trend(student: Student, window: int = 3) -> list[float]:
    """Rolling average of a student's scores across semesters.

    Args:
        student: The student whose trend to compute.
        window: Number of most recent scores to average.

    Returns:
        Rolling averages in semester order. Semesters sort correctly as
        text because of the "YYYY-SN" format.
    """
    ordered = sorted(student.grades, key=lambda grade: grade.semester)
    return rolling_average((grade.score for grade in ordered), window)