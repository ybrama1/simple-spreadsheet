import unittest
from simple_spreadsheet import read_cell

class TestReadCell(unittest.TestCase):
    spreadsheet = [
        ["=B2+5", "=A1-3.5"],
        ["=A1", "42"],
        ["3.14", "=B2"]
    ]
    def test_read_number(self):
        self.assertEqual(read_cell("3.14", self.spreadsheet), 3.14)
        self.assertEqual(read_cell("42", self.spreadsheet), 42.0)

    def test_read_single_reference(self):
        self.assertEqual(read_cell("=A1", self.spreadsheet), 47.0)
        self.assertEqual(read_cell("=B2", self.spreadsheet), 42.0)

    def test_read_expression(self):
        self.assertEqual(read_cell("=A1-3.5", self.spreadsheet), 43.5)
        self.assertEqual(read_cell("=B2+5", self.spreadsheet), 47.0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            read_cell("invalid", self.spreadsheet)
        with self.assertRaises(ValueError):
            read_cell("=A1 +", self.spreadsheet)
        with self.assertRaises(ValueError):
            read_cell("= + 5", self.spreadsheet)

if __name__ == "__main__":
    unittest.main()