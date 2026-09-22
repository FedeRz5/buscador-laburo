import unittest
from types import SimpleNamespace

from tools.convert_salary_excel import (
    INDEX_PATTERNS,
    detect_column_type,
    header_matches,
    parse_sheet,
)


class FakeWorksheet:
    title = "Sheet1"

    def __init__(self, rows):
        self.rows = rows

    def iter_rows(self, min_row=1, max_row=None, values_only=False):
        rows = self.rows[min_row - 1:max_row]
        for row in rows:
            if values_only:
                yield row
            else:
                yield [SimpleNamespace(value=value) for value in row]

    def __getitem__(self, row_number):
        return [SimpleNamespace(value=value) for value in self.rows[row_number - 1]]


class DetectColumnTypeTests(unittest.TestCase):
    def test_index_headers_are_not_misclassified_as_count(self):
        for header in ("Index", "Salary Index", "Engineering Index", "Median salary"):
            with self.subTest(header=header):
                self.assertEqual(detect_column_type(header), "index")

    def test_single_letter_n_only_matches_as_a_token(self):
        self.assertEqual(detect_column_type("Employee n"), "count")
        self.assertEqual(detect_column_type("Engineering"), None)

    def test_count_headers_still_match_common_labels(self):
        for header in ("Count", "Engineering Count", "Cantidad empleados"):
            with self.subTest(header=header):
                self.assertEqual(detect_column_type(header), "count")

    def test_count_inside_word_does_not_make_count_header(self):
        self.assertIsNone(detect_column_type("Accounting Total"))
        self.assertEqual(detect_column_type("Accounting Index"), "index")

    def test_spanish_accented_headers_match(self):
        self.assertEqual(detect_column_type("Índice salarial"), "index")

    def test_patterns_match_whole_tokens(self):
        self.assertTrue(header_matches("índice salarial", INDEX_PATTERNS))
        # No confundir un fragmento de palabra con un encabezado completo.
        self.assertFalse(header_matches("salaryindex", INDEX_PATTERNS))
        self.assertTrue(header_matches("salary index", INDEX_PATTERNS))

    def test_parse_sheet_preserves_category_name_with_letter_n(self):
        ws = FakeWorksheet([
            ("Company", "Engineering Count", "Engineering Index"),
            ("Example Corp", 12, 105.5),
        ])

        companies = parse_sheet(ws)

        self.assertEqual(companies[0]["categories"]["engineering"], {"count": 12, "index": 105.5})

    def test_parse_sheet_groups_accounting_count_index_pair(self):
        ws = FakeWorksheet([
            ("Company", "Accounting Count", "Accounting Index"),
            ("Example Corp", 12, 105.5),
        ])

        companies = parse_sheet(ws)

        self.assertEqual(companies[0]["categories"]["accounting"], {"count": 12, "index": 105.5})

    def test_parse_sheet_normalizes_paired_category_name_with_underscores(self):
        ws = FakeWorksheet([
            ("Company", "Software Engineering Count", "Software Engineering Index"),
            ("Example Corp", 8, 110.0),
        ])

        companies = parse_sheet(ws)

        self.assertEqual(companies[0]["categories"]["software_engineering"], {"count": 8, "index": 110.0})




class ArgentinaSheetTests(unittest.TestCase):
    def test_spanish_headers_and_category_pair(self):
        ws = FakeWorksheet([
            ("Razón social", "Ciudad", "Administración cantidad", "Administración índice"),
            ("Empresa de ejemplo SRL", "Córdoba", 4, 110),
        ])
        row = parse_sheet(ws)[0]
        self.assertEqual(row["city"], "Córdoba")
        self.assertEqual(row["categories"]["administración"], {"count": 4, "index": 110})


if __name__ == "__main__":
    unittest.main()
