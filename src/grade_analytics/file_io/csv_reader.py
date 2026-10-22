"""Load student records from CSV files."""

import csv
from collections.abc import Sequence
from pathlib import Path

from grade_analytics.exceptions import DataFileError, InvalidRecordError, InvalidScoreError
from grade_analytics.models import Course, Grade, Student


REQUIRED_COLUMNS = (
    "student_id", "name", "major", "year",
    "course_code", "course_name", "credits", "semester", "score",
)


def load_students(csv_path: Path | str) -> list[Student]:
    """Read a CSV of grade records and group them into Student objects.

    Each row is one grade: one student, one course, one semester. Rows
    for the same student_id are merged into a single Student, and rows
    for the same course_code share a single Course object.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        Students in the order they first appear in the file.

    Raises:
        DataFileError: If the file is missing, unreadable, not UTF-8,
            or lacks required columns.
        InvalidRecordError: If a row has an empty or invalid value. The
            message includes the line number.
    """
    path = Path(csv_path)
    students: dict[str, Student] = {}
    courses: dict[str, Course] = {}

    try:
        with path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            _check_columns(reader.fieldnames, path)

            for line_number, row in enumerate(reader, start=2):
                _add_row(row, students, courses, f"{path.name}, line {line_number}")
                
    except FileNotFoundError as error:
        raise DataFileError(f"File not found: {path}") from error
    except PermissionError as error:
        raise DataFileError(f"Permission denied: {path}") from error
    except UnicodeDecodeError as error:
        raise DataFileError(f"{path} is not a valid UTF-8 text file") from error
    except OSError as error:
        raise DataFileError(f"Could not read {path}: {error}") from error

    return list(students.values())


def _check_columns(fieldnames: Sequence[str] | None, path: Path) -> None:
    """Raise DataFileError if the CSV header lacks a required column."""
    missing = [
        column 
        for column in REQUIRED_COLUMNS 
        if column not in (fieldnames or [])
    ]
    if missing:
        raise DataFileError(f"{path.name} is missing columns: {', '.join(missing)}")


def _add_row(
    row: dict[str, str],
    students: dict[str, Student],
    courses: dict[str, Course],
    location: str,
) -> None:
    """Turn one CSV row into a Grade and attach it to its Student."""
    values = {
        # dictionary comprehension :-)
        column: (row.get(column) or "").strip() 
        for column in REQUIRED_COLUMNS
    }

    empty = [
        # list compreshension
        column 
        for column, value in values.items() 
        if not value
    ]

    if empty:
        raise InvalidRecordError(f"{location}: empty value for {', '.join(empty)}")

    try:
        student_id = values["student_id"]
        if student_id not in students:
            students[student_id] = Student(
                student_id, values["name"], values["major"], int(values["year"])
            )

        code = values["course_code"]
        if code not in courses:
            courses[code] = Course(code, values["course_name"], int(values["credits"]))

        grade = Grade(courses[code], values["semester"], float(values["score"]))
    except (ValueError, InvalidScoreError) as error:
        raise InvalidRecordError(f"{location}: {error}") from error

    students[student_id].grades.append(grade)

