import pytest

from grade_analytics.models import Course, Grade, Student


@pytest.fixture
def cs201() -> Course:
    return Course("CS201", "Data Structures", 4)


@pytest.fixture
def students(cs201: Course) -> list[Student]:
    return [
        Student("S001", "Aline", "CS", 2,
                [Grade(cs201, "2025-S1", 92), Grade(cs201, "2025-S2", 78)]),
        Student("S002", "Eric", "Econ", 1, [Grade(cs201, "2025-S1", 65)]),
        Student("S003", "Grace", "CS", 1),  # no grades yet
    ]
