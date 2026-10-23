"""Tests for loading students from CSV."""

from collections.abc import Callable
from pathlib import Path

import pytest

from grade_analytics.exceptions import DataFileError, InvalidRecordError, InvalidScoreError
from grade_analytics.file_io import load_students


def test_rows_of_one_student_are_merged(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    second = valid_row.copy()
    second[7] = "2025-S2"
    students = load_students(write_csv([valid_row, second]))
    assert len(students) == 1
    assert len(students[0].grades) == 2


def test_values_are_converted_to_the_right_types(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    student = load_students(write_csv([valid_row]))[0]
    grade = student.grades[0]
    assert (student.year, grade.course.credits, grade.score) == (2, 4, 87.5)


def test_same_course_is_shared_between_students(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    other = valid_row.copy()
    other[0] = "S002"
    first, second = load_students(write_csv([valid_row, other]))
    assert first.grades[0].course is second.grades[0].course


def test_whitespace_around_values_is_removed(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    padded = [f"  {value} " for value in valid_row]
    assert load_students(write_csv([padded]))[0].name == "Aline Uwase"


def test_accepts_a_string_path(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    assert len(load_students(str(write_csv([valid_row])))) == 1


def test_header_only_gives_no_students(write_csv: Callable[..., Path]) -> None:
    assert load_students(write_csv([])) == []


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="File not found"):
        load_students(tmp_path / "nope.csv")


def test_missing_columns(write_csv: Callable[..., Path]) -> None:
    path = write_csv([["S001", "Aline"]], header=["student_id", "name"])
    with pytest.raises(DataFileError, match="missing columns: major"):
        load_students(path)


def test_empty_value_reports_line_number(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    broken = valid_row.copy()
    broken[2] = ""
    with pytest.raises(InvalidRecordError, match="line 3: empty value for major"):
        load_students(write_csv([valid_row, broken]))


@pytest.mark.parametrize(("column", "value"), [(3, "second"), (6, "four"), (8, "abc")])
def test_non_numeric_values(
    write_csv: Callable[..., Path], valid_row: list[str], column: int, value: str
) -> None:
    broken = valid_row.copy()
    broken[column] = value
    with pytest.raises(InvalidRecordError, match="line 2"):
        load_students(write_csv([broken]))


def test_out_of_range_score_keeps_original_cause(write_csv: Callable[..., Path], valid_row: list[str]) -> None:
    broken = valid_row.copy()
    broken[8] = "150"
    with pytest.raises(InvalidRecordError) as caught:
        load_students(write_csv([broken]))
    assert isinstance(caught.value.__cause__, InvalidScoreError)


def test_file_that_is_not_utf8(tmp_path: Path) -> None:
    path = tmp_path / "latin1.csv"
    path.write_bytes(
        b"student_id,name,major,year,course_code,course_name,credits,semester,score\n"
        b"S001,Ren\xe9,CS,1,CS201,DS,4,2025-S1,80\n"
    )
    with pytest.raises(DataFileError, match="UTF-8"):
        load_students(path)


def test_permission_denied(
    write_csv: Callable[..., Path], valid_row: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    path = write_csv([valid_row])

    def deny(*args: object, **kwargs: object) -> None:
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "open", deny)
    with pytest.raises(DataFileError, match="Permission denied"):
        load_students(path)