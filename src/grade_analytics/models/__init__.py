"""Data models for students, courses and grades."""

from .course import Course
from .grade import Grade
from .student import Student

__all__ = ["Course", "Grade", "Student"]