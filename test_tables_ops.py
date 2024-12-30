import unittest
import subprocess
import os
import csv
from collections import Counter


class TestTableOps(unittest.TestCase):
    TEST_DATA_DIR = "test-data"

    def _run_command(self, command, input_data=None):
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE if input_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Important for handling text I/O
        )
        stdout, stderr = process.communicate(input_data)
        return process.returncode, stdout, stderr

    def _compare_tsv(self, expected_file, actual_output):
        with open(os.path.join(self.TEST_DATA_DIR, expected_file), 'r', encoding='utf-8') as f:
            expected_lines = list(csv.reader(f, delimiter='\t'))
        actual_lines = list(csv.reader(actual_output.splitlines(), delimiter='\t'))
        self.assertEqual(expected_lines, actual_lines)

    def test_table_union_union(self):
        returncode, stdout, stderr = self._run_command(
            ["table-union", os.path.join(self.TEST_DATA_DIR, "union1.tsv"), os.path.join(self.TEST_DATA_DIR, "union2.tsv")]
        )
        self.assertEqual(returncode, 0)
        self._compare_tsv("union_expected.tsv", stdout)
        self.assertEqual(stderr, "")

    def test_table_union_join(self):
        returncode, stdout, stderr = self._run_command(
            ["table-union", "--no-union", os.path.join(self.TEST_DATA_DIR, "users.tsv"), os.path.join(self.TEST_DATA_DIR, "orders.tsv")]
        )
        self.assertEqual(returncode, 0)
        self._compare_tsv("merged_expected.tsv", stdout)
        self.assertEqual(stderr, "")

    def test_table_summarize(self):
        returncode, stdout, stderr = self._run_command(["table-summarize", os.path.join(self.TEST_DATA_DIR, "data_summarize.tsv")])
        self.assertEqual(returncode, 0)

        expected_summary = """Summary:
Category:
\t - A: 3 of 6
\t - B: 2 of 6
\t - C: 1 of 6
Value:
\t - 10: 1 of 6
\t - 12: 1 of 6
\t - 15: 1 of 6
\t - 20: 1 of 6
\t - 25: 1 of 6
\t - 30: 1 of 6
"""
        self.assertEqual(stdout.strip(), expected_summary.strip())
        self.assertEqual(stderr, "")

    def test_table_sort(self):
        returncode, stdout, stderr = self._run_command(
            ["table-sort", "-k", "Age", "-k", "Name", os.path.join(self.TEST_DATA_DIR, "data_sort.tsv")]
        )
        self.assertEqual(returncode, 0)
        self._compare_tsv("sorted_data_expected.tsv", stdout)
        self.assertEqual(stderr, "")

    def test_table_sort_pipe(self):
        with open(os.path.join(self.TEST_DATA_DIR, "data_sort.tsv"), 'r', encoding="utf-8") as infile:
            input_data = infile.read()
        returncode, stdout, stderr = self._run_command(
            ["table-sort", "-k", "Age", "-k", "Name"], input_data
        )
        self.assertEqual(returncode, 0)
        self._compare_tsv("sorted_data_expected.tsv", stdout)
        self.assertEqual(stderr, "")


if __name__ == "__main__":
    unittest.main()