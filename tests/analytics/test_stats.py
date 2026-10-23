"""Tests for the descriptive statistics.

Our implementations are checked against Python's own statistics module,
which acts as a trusted reference.
"""

import random
import statistics
from collections.abc import Callable, Sequence

import pytest

from grade_analytics.analytics import mean, median, mode, percentile_rank
from grade_analytics.exceptions import InsufficientDataError


def random_scores(seed: int) -> list[float]:
    """100 integer scores between 50 and 100, so repeats are guaranteed."""
    rng = random.Random(seed)
    return [float(rng.randint(50, 100)) for _ in range(100)]


@pytest.mark.parametrize("seed", range(10))
def test_matches_the_standard_library(seed: int) -> None:
    scores = random_scores(seed)
    assert mean(scores) == pytest.approx(statistics.mean(scores))
    assert median(scores) == statistics.median(scores)
    assert mode(scores) == sorted(statistics.multimode(scores))


def test_median_odd_count() -> None:
    assert median([90, 70, 80]) == 80.0


def test_median_even_count_averages_middle_values() -> None:
    assert median([70, 90, 80, 100]) == 85.0


def test_mode_returns_all_tied_values() -> None:
    assert mode([80, 90, 90, 70, 80]) == [80, 90]


def test_mode_without_repeats_is_empty() -> None:
    assert mode([70, 80, 90]) == []


def test_mode_of_single_value() -> None:
    assert mode([75]) == [75]


@pytest.mark.parametrize(
    ("score", "expected"),
    [(80, 62.5), (60, 12.5), (90, 87.5), (85, 75.0), (100, 100.0), (10, 0.0)],
)
def test_percentile_rank(score: float, expected: float) -> None:
    assert percentile_rank(score, [60, 70, 80, 90]) == expected


def test_percentile_rank_when_everyone_is_equal() -> None:
    assert percentile_rank(75, [75, 75, 75]) == 50.0


@pytest.mark.parametrize("function", [mean, median, mode])
def test_empty_data_raises(function: Callable[[Sequence[float]], object]) -> None:
    with pytest.raises(InsufficientDataError):
        function([])


def test_percentile_rank_of_empty_data_raises() -> None:
    with pytest.raises(InsufficientDataError):
        percentile_rank(80, [])