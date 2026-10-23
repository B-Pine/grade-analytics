"""Tests for the command-line interface, calling main() directly."""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from grade_analytics.cli import main


def test_success_writes_report_and_prints_summary(
    write_csv: Callable[..., Path], valid_row: list[str],
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "out.json"
    assert main([str(write_csv([valid_row])), "-o", str(output)]) == 0
    assert output.exists()
    assert "Top performers" in capsys.readouterr().out


def test_top_option_limits_performers(
    write_csv: Callable[..., Path], valid_row: list[str], tmp_path: Path
) -> None:
    other = valid_row.copy()
    other[0] = "S002"
    output = tmp_path / "out.json"
    main([str(write_csv([valid_row, other])), "-o", str(output), "--top", "1"])
    assert len(json.loads(output.read_text(encoding="utf-8"))["top_performers"]) == 1


def test_data_error_returns_1_and_prints_to_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "missing.csv")]) == 1
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.err
    assert captured.out == ""


@pytest.mark.parametrize("value", ["0", "-3", "abc"])
def test_invalid_top_exits_with_code_2(value: str, tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as caught:
        main([str(tmp_path / "x.csv"), "--top", value])
    assert caught.value.code == 2