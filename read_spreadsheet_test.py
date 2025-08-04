import unittest
from simple_spreadsheet import read_spreadsheet

class TestReadSpreadsheet(unittest.TestCase):

    def test_valid_spreadsheet(self):
        spreadsheet = [
            ["=B2+5", "=A1-3.5"],
            ["=A1", "42"],
            ["3.14", "=B2"]
        ]
        self.assertEqual(read_spreadsheet(spreadsheet), [
            [47.0, 43.5],
            [47.0, 42.0],
            [3.14, 42.0]
        ])
    def test_invalid_spreadsheet(self):
        spreadsheet = [
            ["=B2+5", "=A1-3.5"],
            ["=A1", "42"],
            ["3.14", "=B2"],
            ["=A1+5", "A3"]
        ]
        with self.assertRaises(ValueError):
            read_spreadsheet(spreadsheet)

if __name__ == "__main__":
    unittest.main()