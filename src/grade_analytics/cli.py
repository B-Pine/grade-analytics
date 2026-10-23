"""Command-line interface for the grade analytics tool.

Usage:
    grade-analytics data/students.csv
    grade-analytics data/students.csv -o reports/summary.json --top 10
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .exceptions import GradeAnalyticsError
from .file_io import load_students, write_report
from .reports import build_summary
from .schemas import SummaryReport

BAR_WIDTH = 30


def main(argv: Sequence[str] | None = None) -> int:
    """Run the tool: load the CSV, build the report, write it, print a summary.

    Args:
        argv: Command-line arguments. Defaults to sys.argv when None.

    Returns:
        Exit code: 0 on success, 1 if the data could not be processed.
        Invalid arguments exit with code 2 (handled by argparse).
    """
    args = _build_parser().parse_args(argv)

    try:
        students = load_students(args.csv)
        report = build_summary(students, args.csv, top_n=args.top)
        path = write_report(report, args.output)
    except GradeAnalyticsError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    _print_summary(report, path)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    """Define the command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="grade-analytics",
        description="Analyze student grades from a CSV file and write a JSON report.",
    )
    parser.add_argument("csv", type=Path, help="path to the student grades CSV file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("reports/summary.json"),
        help="where to write the JSON report (default: reports/summary.json)",
    )
    parser.add_argument(
        "--top",
        type=_positive_int,
        default=5,
        help="number of top performers to include (default: 5)",
    )
    return parser


def _positive_int(value: str) -> int:
    """argparse type that only accepts integers of 1 or more."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1, got {number}")
    return number


def _print_summary(report: SummaryReport, path: Path) -> None:
    """Print a short, human-readable version of the report."""
    stats = report["overall_statistics"]
    print(f"\nGrade Analytics: {report['source_file']}")
    print(f"Students: {report['total_students']}", end="")
    if stats:
        print(f" | Grades: {stats['count']} | Mean: {stats['mean']} | Median: {stats['median']}")
    else:
        print(" | No grades recorded")

    distribution = report["grade_distribution"]
    total = sum(distribution.values()) or 1
    print("\nGrade distribution")
    for letter, count in distribution.items():
        bar = "█" * round(count / total * BAR_WIDTH)
        print(f"  {letter}  {bar:<{BAR_WIDTH}} {count}")

    print("\nTop performers")
    for student in report["top_performers"]:
        print(
            f"  #{student['rank']:<3} {student['name']:<22} "
            f"{student['major']:<20} {student['average']:>6}  (p{student['percentile']:.0f})"
        )

    print(f"\nReport written to {path}")