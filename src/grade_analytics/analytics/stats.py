"""Descriptive statistics for score data: mean, median, mode, percentiles.

Results are returned at full precision. Rounding is left to whoever
displays them, such as the report builder.
"""

from collections import Counter
from collections.abc import Sequence

from ..exceptions import InsufficientDataError


def mean(scores: Sequence[float]) -> float:
    """Arithmetic mean of the scores.

    Raises:
        InsufficientDataError: If scores is empty.

    Example:
        >>> mean([80, 90, 70])
        80.0
    """
    _require_data(scores, "mean")   # give specialized error message
    return sum(scores) / len(scores)


def median(scores: Sequence[float]) -> float:
    """Middle value of the sorted scores.

    With an even number of scores, the two middle values are averaged.

    Raises:
        InsufficientDataError: If scores is empty.

    Example:
        >>> median([70, 90, 80, 100])
        85.0
    """
    _require_data(scores, "median")
    ordered = sorted(scores)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return float(ordered[middle])
    return (ordered[middle - 1] + ordered[middle]) / 2


def mode(scores: Sequence[float]) -> list[float]:
    """Most frequent score(s), sorted ascending.

    Returns every value tied for the highest count, since data can have
    several modes. If no value repeats, there is no mode and an empty
    list is returned (unless there is only one score).

    Raises:
        InsufficientDataError: If scores is empty.

    Example:
        >>> mode([80, 90, 90, 70, 80])
        [80, 90]
        >>> mode([70, 80, 90])
        []
    """
    _require_data(scores, "mode")
    counts = Counter(scores)
    highest = max(counts.values())
    if highest == 1 and len(scores) > 1:
        return []
    return sorted(value for value, count in counts.items() if count == highest)


def percentile_rank(score: float, scores: Sequence[float]) -> float:
    """Percentage of scores below the given score, counting ties as half.

    Uses the mid-rank definition: (below + 0.5 * equal) / total * 100.

    Raises:
        InsufficientDataError: If scores is empty.

    Example:
        >>> percentile_rank(80, [60, 70, 80, 90])
        62.5
    """
    _require_data(scores, "percentile rank")
    below = sum(1 for value in scores if value < score)
    equal = sum(1 for value in scores if value == score)
    return (below + 0.5 * equal) / len(scores) * 100


def _require_data(scores: Sequence[float], operation: str) -> None:
    """Raise InsufficientDataError if there are no scores."""
    if not scores:
        raise InsufficientDataError(f"Cannot compute {operation} of an empty dataset")