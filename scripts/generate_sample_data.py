"""Generate a realistic sample dataset of student grades.

Usage:
    python scripts/generate_sample_data.py                     # 60 students
    python scripts/generate_sample_data.py --students 200 -o data/large.csv

The same --seed always produces the same file, so results are reproducible.
"""

import argparse
import csv
import random
from pathlib import Path

FIRST_NAMES = [
    "Aline", "Eric", "Grace", "Jean", "Divine", "Patrick", "Ange", "Kevin",
    "Claudine", "Olivier", "Esther", "Yves", "Sandrine", "Fabrice", "Nadia",
    "David", "Chantal", "Samuel", "Josiane", "Emmanuel", "Liliane", "Thierry",
]
LAST_NAMES = [
    "Uwase", "Mugisha", "Ineza", "Niyonzima", "Habimana", "Mukamana",
    "Nkurunziza", "Iradukunda", "Hakizimana", "Uwimana", "Ndayisaba", "Kayitesi",
]
COURSES = {
    "Computer Science": [
        ("CS101", "Intro to Programming", 4), ("CS201", "Data Structures", 4),
        ("CS202", "Algorithms", 4), ("CS301", "Databases", 3),
    ],
    "Economics": [
        ("EC101", "Microeconomics", 3), ("EC102", "Macroeconomics", 3),
        ("EC201", "Econometrics", 4), ("EC301", "Development Economics", 3),
    ],
    "Mathematics": [
        ("MA201", "Linear Algebra", 4), ("MA202", "Probability", 3),
        ("MA301", "Real Analysis", 4), ("MA302", "Statistics", 3),
    ],
    "Business": [
        ("BU101", "Principles of Management", 3), ("BU201", "Accounting", 3),
        ("BU202", "Marketing", 3), ("BU301", "Finance", 4),
    ],
}
SHARED_COURSES = [("MA101", "Calculus I", 3), ("EN101", "Academic Writing", 2)]
SEMESTERS = ["2024-S1", "2024-S2", "2025-S1", "2025-S2"]
COLUMNS = [
    "student_id", "name", "major", "year",
    "course_code", "course_name", "credits", "semester", "score",
]


def generate_rows(student_count: int, rng: random.Random) -> list[dict[str, object]]:
    """Create one row per grade for student_count students."""
    rows: list[dict[str, object]] = []
    for number in range(1, student_count + 1):
        major = rng.choice(list(COURSES))
        ability = rng.gauss(74, 9)      # each student has a typical level
        momentum = rng.uniform(-3, 3)   # and improves or declines over time
        courses = COURSES[major] + SHARED_COURSES

        for index, semester in enumerate(SEMESTERS):
            for code, name, credits in rng.sample(courses, k=rng.randint(2, 3)):
                raw = ability + momentum * index + rng.gauss(0, 7)
                score = round(min(100, max(35, raw)) * 2) / 2   # nearest 0.5
                rows.append({
                    "student_id": f"S{number:03d}",
                    "name": f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
                    "major": major,
                    "year": rng.randint(1, 4),
                    "course_code": code,
                    "course_name": name,
                    "credits": credits,
                    "semester": semester,
                    "score": score,
                })
    return _keep_student_details_consistent(rows)


def _keep_student_details_consistent(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Give every row of a student the same name and year as their first row."""
    first_seen: dict[object, dict[str, object]] = {}
    for row in rows:
        first = first_seen.setdefault(row["student_id"], row)
        row["name"], row["year"] = first["name"], first["year"]
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample student grade data.")
    parser.add_argument("--students", type=int, default=60, help="number of students (default: 60)")
    parser.add_argument("-o", "--output", type=Path, default=Path("data/students.csv"))
    parser.add_argument("--seed", type=int, default=42, help="random seed (default: 42)")
    args = parser.parse_args()

    rows = generate_rows(args.students, random.Random(args.seed))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} grade records for {args.students} students to {args.output}")


if __name__ == "__main__":
    main()
