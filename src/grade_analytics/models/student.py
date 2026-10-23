"""Student model."""

from dataclasses import dataclass, field
from typing import Optional

from .grade import Grade


@dataclass(slots=True)
class Student:
    """A student and the grades they have obtained.

    Mutable, so grades can be appended while records are being loaded.

    Attributes:
        student_id: Unique identifier, e.g. "S001".
        name: Full name.
        major: Field of study, e.g. "Computer Science".
        year: Current year of study (1, 2, 3...).
        grades: Grades obtained so far. Each student gets its own list.

    Example:
        >>> from grade_analytics.models import Course, Grade
        >>> cs = Course("CS201", "Data Structures", 4)
        >>> s = Student("S001", "Aline", "CS", 2, [Grade(cs, "2025-S1", 90)])
        >>> s.average()
        90.0
    """

    student_id: str
    name: str
    major: str
    year: int
    grades: list[Grade] = field(default_factory=list)

    def average(self) -> Optional[float]:
        """Mean score across all of the student's grades.

        Returns:
            The average score, or None if the student has no grades yet.
        """
        if not self.grades:
            return None
        return sum(g.score for g in self.grades) / len(self.grades)