import csv
from pathlib import Path


def load_grades(path: str | Path) -> list[dict]:
    """Load student grades from a CSV file."""
    path = Path(path)
    records = []

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"student_id", "name", "score"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain student_id, name, and score columns")

        for row in reader:
            score = float(row["score"])
            if not 0 <= score <= 100:
                raise ValueError(f"Invalid score for {row['student_id']}: {score}")
            records.append(
                {
                    "student_id": row["student_id"],
                    "name": row["name"],
                    "score": score,
                }
            )

    if not records:
        raise ValueError("CSV contains no student records")

    return records


def average_score(records: list[dict]) -> float:
    return sum(record["score"] for record in records) / len(records)


def highest_score(records: list[dict]) -> dict:
    return max(records, key=lambda record: record["score"])


def lowest_score(records: list[dict]) -> dict:
    return min(records, key=lambda record: record["score"])


def count_passed(records: list[dict], passing_score: float = 60.0) -> int:
    return sum(record["score"] >= passing_score for record in records)


def count_failed(records: list[dict], passing_score: float = 60.0) -> int:
    return len(records) - count_passed(records, passing_score)
