from pathlib import Path

from . import (
    average_score,
    count_failed,
    count_passed,
    highest_score,
    load_grades,
    lowest_score,
)


def main() -> None:
    data_path = Path(__file__).resolve().parents[2] / "data" / "grades.csv"
    records = load_grades(data_path)

    best = highest_score(records)
    lowest = lowest_score(records)
    passed = count_passed(records)
    failed = count_failed(records)
    pass_rate = 100 * passed / len(records)

    print("STUDENT GRADE ANALYZER")
    print("=" * 46)
    print(f"Students:       {len(records)}")
    print(f"Average score:  {average_score(records):.2f}")
    print(f"Highest score:  {best['name']} ({best['score']:.1f})")
    print(f"Lowest score:   {lowest['name']} ({lowest['score']:.1f})")
    print(f"Passed:         {passed}")
    print(f"Failed:         {failed}")
    print(f"Pass rate:      {pass_rate:.1f}%")

    print("\nTOP 5 STUDENTS")
    print("-" * 46)
    for position, record in enumerate(
        sorted(records, key=lambda item: item["score"], reverse=True)[:5],
        start=1,
    ):
        print(f"{position:>2}. {record['name']:<24} {record['score']:>5.1f}")


if __name__ == "__main__":
    main()
