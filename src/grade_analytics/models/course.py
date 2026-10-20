"""Course model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Course:
    """An academic course.

    Immutable and hashable, so it can be used in sets and as a dict key.

    Attributes:
        code: Unique course code, e.g. "CS201".
        name: Human-readable course name.
        credits: Number of credit hours.
    """

    code: str
    name: str
    credits: int