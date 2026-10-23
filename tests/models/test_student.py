"""Tests for the Student model."""

from grade_analytics.models import Course, Grade, Student


def test_average_of_grades(course: Course) -> None:
    student = Student("S1", "Aline", "CS", 2,
                      [Grade(course, "2025-S1", 90), Grade(course, "2025-S1", 80)])
    assert student.average() == 85.0


def test_average_without_grades_is_none() -> None:
    assert Student("S1", "Aline", "CS", 2).average() is None


def test_each_student_gets_its_own_grade_list() -> None:
    a = Student("S1", "Aline", "CS", 2)
    b = Student("S2", "Eric", "CS", 2)
    assert a.grades is not b.grades


def test_grades_can_be_added_after_creation(course: Course) -> None:
    student = Student("S1", "Aline", "CS", 2)
    student.grades.append(Grade(course, "2025-S1", 70))
    assert student.average() == 70.0