"""Tests for the Course model."""

import dataclasses

import pytest

from grade_analytics.models import Course


def test_stores_its_fields() -> None:
    course = Course("CS201", "Data Structures", 4)
    assert (course.code, course.name, course.credits) == ("CS201", "Data Structures", 4)


def test_is_immutable() -> None:
    course = Course("CS201", "Data Structures", 4)
    with pytest.raises(dataclasses.FrozenInstanceError):
        course.credits = 5  # type: ignore[misc]


def test_equal_courses_are_deduplicated_in_a_set() -> None:
    a = Course("CS201", "Data Structures", 4)
    b = Course("CS201", "Data Structures", 4)
    assert a == b
    assert len({a, b}) == 1


def test_uses_slots_instead_of_a_dict() -> None:
    assert not hasattr(Course("CS201", "Data Structures", 4), "__dict__")