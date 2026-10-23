"""Run the >>> examples inside docstrings as tests.

If a function changes and its documented example stops being true,
this test fails, so the documentation can never silently go stale.
"""

import doctest
from types import ModuleType

import pytest

from grade_analytics.analytics import aggregators, stats
from grade_analytics.models import course, grade, student


@pytest.mark.parametrize("module", [course, grade, student, aggregators, stats],
                         ids=lambda m: m.__name__)
def test_docstring_examples(module: ModuleType) -> None:
    result = doctest.testmod(module)
    assert result.attempted > 0, "no examples found"
    assert result.failed == 0
