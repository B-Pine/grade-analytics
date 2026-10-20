"""Grade model."""

from dataclasses import dataclass

from ..exceptions import InvalidScoreError
from .course import Course


@dataclass(frozen=True, slots=True)
class Grade:
    """A score obtained in a course during a given semester.

    Immutable: once recorded, a grade cannot be modified.

    Attributes:
        course: The course the grade belongs to.
        semester: Semester identifier in the format "YYYY-SN", e.g. "2025-S1".
        score: Numeric score between 0 and 100 inclusive.

    Raises:
        InvalidScoreError: If the score is outside the 0–100 range.

    Example:
        >>> cs = Course("CS201", "Data Structures", 4)
        >>> Grade(cs, "2025-S1", 87.5).letter
        'B'
    """

    course: Course
    semester: str
    score: float

    def __post_init__(self) -> None:
        """Validate the score right after the instance is created."""
        if not 0 <= self.score <= 100:
            raise InvalidScoreError(f"Score must be 0 - 100, got {self.score}")

    @property
    def letter(self) -> str:
        """Letter grade for the score.

        Returns:
            "A" (90+), "B" (80+), "C" (70+), "D" (60+) or "F" (below 60).
        """
        if self.score >= 90:
            return "A"
        if self.score >= 80:
            return "B"
        if self.score >= 70:
            return "C"
        if self.score >= 60:
            return "D"
        return "F"