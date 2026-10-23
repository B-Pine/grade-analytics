"""Tests for writing reports as JSON."""

import json
from pathlib import Path

import pytest

from grade_analytics.exceptions import DataFileError
from grade_analytics.file_io import write_report
from grade_analytics.models import Student
from grade_analytics.reports import build_summary
from grade_analytics.schemas import SummaryReport


@pytest.fixture
def report(students: list[Student]) -> SummaryReport:
    return build_summary(students, "grades.csv")


def test_written_json_reads_back_identical(report: SummaryReport, tmp_path: Path) -> None:
    path = write_report(report, tmp_path / "summary.json")
    assert json.loads(path.read_text(encoding="utf-8")) == report


def test_creates_missing_folders(report: SummaryReport, tmp_path: Path) -> None:
    path = write_report(report, tmp_path / "a" / "b" / "summary.json")
    assert path.exists()


def test_keeps_accented_characters_readable(report: SummaryReport, tmp_path: Path) -> None:
    report["source_file"] = "élèves.csv"
    path = write_report(report, tmp_path / "summary.json")
    assert "élèves.csv" in path.read_text(encoding="utf-8")


def test_unwritable_location(report: SummaryReport, tmp_path: Path) -> None:
    blocker = tmp_path / "not_a_folder"
    blocker.write_text("I am a file")
    with pytest.raises(DataFileError):
        write_report(report, blocker / "summary.json")