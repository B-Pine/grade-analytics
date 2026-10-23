"""Compare the memory and speed of different data structure choices.

Usage:
    python scripts/compare_memory.py

Prints Markdown tables, ready to paste into the README. Numbers vary
by machine and Python version, so always report your own.
"""

import sys
import timeit
import tracemalloc
from collections import deque, namedtuple
from collections.abc import Callable
from dataclasses import dataclass

RECORDS = 100_000
SCORES = 1_000_000


@dataclass
class PlainRecord:
    student_id: str
    name: str
    major: str
    year: int


@dataclass(slots=True)
class SlottedRecord:
    student_id: str
    name: str
    major: str
    year: int


TupleRecord = namedtuple("TupleRecord", "student_id name major year")


def memory_used(build: Callable[[], object]) -> int:
    """Bytes still allocated after build() runs, i.e. the size of its result."""
    tracemalloc.start()
    result = build()
    current, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del result
    return current


def peak_memory(work: Callable[[], object]) -> int:
    """Highest number of bytes allocated at any moment while work() runs."""
    tracemalloc.start()
    work()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def compare_records() -> None:
    """Memory for 100,000 student records in four representations."""
    ids = [f"S{i:06d}" for i in range(RECORDS)]   # built outside the measurement
    name, major, year = "Aline Uwase", "Computer Science", 2

    builders: dict[str, Callable[[], object]] = {
        "dict": lambda: [
            {"student_id": i, "name": name, "major": major, "year": year} for i in ids
        ],
        "dataclass": lambda: [PlainRecord(i, name, major, year) for i in ids],
        "namedtuple": lambda: [TupleRecord(i, name, major, year) for i in ids],
        "dataclass(slots=True)": lambda: [SlottedRecord(i, name, major, year) for i in ids],
    }
    results = {label: memory_used(build) for label, build in builders.items()}
    baseline = results["dict"]

    print(f"### Storing {RECORDS:,} student records\n")
    print("| Representation | Total memory | Per record | vs dict |")
    print("|---|---|---|---|")
    for label, total in results.items():
        print(f"| `{label}` | {total / 1_048_576:.1f} MB | {total // RECORDS} bytes "
              f"| {total / baseline:.0%} |")
    print()


def compare_list_and_generator() -> None:
    """Peak memory when summing 1,000,000 scores."""
    as_list = peak_memory(lambda: sum([float(i % 100) for i in range(SCORES)]))
    as_generator = peak_memory(lambda: sum(float(i % 100) for i in range(SCORES)))

    print(f"### Summing {SCORES:,} scores\n")
    print("| Approach | Peak memory |")
    print("|---|---|")
    print(f"| list comprehension `sum([...])` | {as_list / 1_048_576:.1f} MB |")
    print(f"| generator expression `sum(...)` | {as_generator / 1024:.1f} KB |")
    print()


def compare_sliding_windows() -> None:
    """Time to slide a 10,000-value window over 100,000 scores."""
    window, values = 10_000, range(100_000)

    def with_deque() -> None:
        recent: deque[int] = deque(maxlen=window)
        for value in values:
            recent.append(value)

    def with_list() -> None:
        recent: list[int] = []
        for value in values:
            recent.append(value)
            if len(recent) > window:
                recent.pop(0)

    deque_time = min(timeit.repeat(with_deque, number=1, repeat=3))
    list_time = min(timeit.repeat(with_list, number=1, repeat=3))

    print(f"### Sliding a {window:,}-value window over {len(values):,} scores\n")
    print("| Approach | Time |")
    print("|---|---|")
    print(f"| `deque(maxlen=...)` | {deque_time * 1000:.1f} ms |")
    print(f"| `list` + `pop(0)` | {list_time * 1000:.1f} ms ({list_time / deque_time:.0f}x slower) |")
    print()


if __name__ == "__main__":
    print(f"Python {sys.version.split()[0]} on {sys.platform}\n")
    compare_records()
    compare_list_and_generator()
    compare_sliding_windows()