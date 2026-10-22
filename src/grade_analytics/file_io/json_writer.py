"""Write reports to disk as JSON."""

import json
from pathlib import Path

from grade_analytics.exceptions import DataFileError
from grade_analytics.schemas import SummaryReport


def write_report(report: SummaryReport, output_path: Path | str) -> Path:
    """Write a report as pretty-printed JSON.

    Missing parent folders are created automatically.

    Args:
        report: The report to write.
        output_path: Destination file, e.g. "reports/summary.json".

    Returns:
        The path the report was written to.

    Raises:
        DataFileError: If the file or its folder cannot be written.
    """
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=2, ensure_ascii=False)
            
    except PermissionError as error:
        raise DataFileError(f"Permission denied: {path}") from error
    except OSError as error:
        raise DataFileError(f"Could not write {path}: {error}") from error
    return path