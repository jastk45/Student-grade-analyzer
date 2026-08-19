import csv
import tempfile
import unittest
from pathlib import Path

from grades import (
    average_score,
    count_failed,
    count_passed,
    highest_score,
    load_grades,
    lowest_score,
)


class LoadGradesTests(unittest.TestCase):
    def write_csv(self, fieldnames, rows):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        path = Path(temporary_directory.name) / "grades.csv"

        with path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return path

    def test_load_grades_returns_normalized_records_from_valid_csv(self):
        path = self.write_csv(
            ["student_id", "name", "score", "course"],
            [
                {
                    "student_id": "STU001",
                    "name": "Ana Garcia",
                    "score": "72.5",
                    "course": "Math",
                }
            ],
        )

        records = load_grades(path)

        self.assertEqual(
            records,
            [{"student_id": "STU001", "name": "Ana Garcia", "score": 72.5}],
        )

    def test_load_grades_accepts_string_path(self):
        path = self.write_csv(
            ["student_id", "name", "score"],
            [{"student_id": "STU001", "name": "Ana Garcia", "score": "60"}],
        )

        records = load_grades(str(path))

        self.assertEqual(records[0]["score"], 60.0)

    def test_load_grades_rejects_missing_required_columns(self):
        path = self.write_csv(
            ["student_id", "name"],
            [{"student_id": "STU001", "name": "Ana Garcia"}],
        )

        with self.assertRaisesRegex(ValueError, "student_id, name, and score"):
            load_grades(path)

    def test_load_grades_rejects_csv_without_student_rows(self):
        path = self.write_csv(["student_id", "name", "score"], [])

        with self.assertRaisesRegex(ValueError, "no student records"):
            load_grades(path)

    def test_load_grades_accepts_scores_at_valid_boundaries(self):
        path = self.write_csv(
            ["student_id", "name", "score"],
            [
                {"student_id": "STU001", "name": "Zero", "score": "0"},
                {"student_id": "STU002", "name": "Perfect", "score": "100"},
            ],
        )

        records = load_grades(path)

        self.assertEqual([record["score"] for record in records], [0.0, 100.0])

    def test_load_grades_rejects_scores_outside_valid_range(self):
        for score in ("-0.1", "100.1"):
            with self.subTest(score=score):
                path = self.write_csv(
                    ["student_id", "name", "score"],
                    [{"student_id": "STU001", "name": "Ana Garcia", "score": score}],
                )

                with self.assertRaisesRegex(ValueError, "Invalid score for STU001"):
                    load_grades(path)

    def test_load_grades_rejects_non_numeric_score(self):
        path = self.write_csv(
            ["student_id", "name", "score"],
            [{"student_id": "STU001", "name": "Ana Garcia", "score": "excellent"}],
        )

        with self.assertRaises(ValueError):
            load_grades(path)

    def test_load_grades_raises_file_not_found_for_missing_path(self):
        missing_path = Path(tempfile.gettempdir()) / "missing-grades-file.csv"

        with self.assertRaises(FileNotFoundError):
            load_grades(missing_path)


class GradeStatisticsTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"student_id": "STU001", "name": "Ana", "score": 60.0},
            {"student_id": "STU002", "name": "Luis", "score": 80.0},
            {"student_id": "STU003", "name": "Sofia", "score": 40.0},
        ]

    def test_average_score_calculates_mean_for_multiple_decimal_scores(self):
        records = [
            {"student_id": "STU001", "name": "Ana", "score": 70.5},
            {"student_id": "STU002", "name": "Luis", "score": 80.0},
        ]

        self.assertEqual(average_score(records), 75.25)

    def test_average_score_returns_only_record_score(self):
        record = [{"student_id": "STU001", "name": "Ana", "score": 72.5}]

        self.assertEqual(average_score(record), 72.5)

    def test_average_score_rejects_empty_records(self):
        with self.assertRaises(ZeroDivisionError):
            average_score([])

    def test_highest_score_returns_full_record_with_highest_score(self):
        self.assertEqual(highest_score(self.records), self.records[1])

    def test_lowest_score_returns_full_record_with_lowest_score(self):
        self.assertEqual(lowest_score(self.records), self.records[2])

    def test_extreme_score_functions_keep_first_record_on_tie(self):
        tied_records = [
            {"student_id": "STU001", "name": "First", "score": 80.0},
            {"student_id": "STU002", "name": "Second", "score": 80.0},
        ]

        self.assertIs(highest_score(tied_records), tied_records[0])
        self.assertIs(lowest_score(tied_records), tied_records[0])

    def test_extreme_score_functions_reject_empty_records(self):
        for function in (highest_score, lowest_score):
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError):
                    function([])

    def test_count_passed_uses_default_threshold_inclusively(self):
        self.assertEqual(count_passed(self.records), 2)

    def test_count_passed_accepts_custom_decimal_threshold(self):
        self.assertEqual(count_passed(self.records, passing_score=80.0), 1)

    def test_count_failed_is_complement_of_passed_records(self):
        passed = count_passed(self.records, passing_score=60.0)

        self.assertEqual(count_failed(self.records, passing_score=60.0), 1)
        self.assertEqual(passed + count_failed(self.records, passing_score=60.0), len(self.records))

    def test_count_functions_return_zero_for_empty_records(self):
        self.assertEqual(count_passed([]), 0)
        self.assertEqual(count_failed([]), 0)


if __name__ == "__main__":
    unittest.main()
