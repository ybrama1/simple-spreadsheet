import unittest
from simple_spreadsheet import parse_cell

class TestParseCell(unittest.TestCase):

    def test_parse_number(self):
        self.assertEqual(parse_cell("42"), (None, None, 42.0))
        self.assertEqual(parse_cell("3.14"), (None, None, 3.14))

    def test_parse_single_reference(self):
        self.assertEqual(parse_cell("=A1"), ("A1", None, None))
        self.assertEqual(parse_cell("=B2"), ("B2", None, None))

    def test_parse_expression(self):
        self.assertEqual(parse_cell("=A1+5"), ("A1", "+", 5.0))
        self.assertEqual(parse_cell("=B2-3.5"), ("B2", "-", 3.5))
        self.assertEqual(parse_cell("=2.5+C3"), (2.5, "+", "C3"))
        self.assertEqual(parse_cell("=A1-B2"), ("A1", "-", "B2"))

    def test_empty_cell(self):
        self.assertEqual(parse_cell(""), (None, None, 0))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_cell("invalid")
        with self.assertRaises(ValueError):
            parse_cell("=A1 +")
        with self.assertRaises(ValueError):
            parse_cell("= + 5")
        with self.assertRaises(ValueError):
            parse_cell("=A1 + B2 + 3")
        with self.assertRaises(ValueError):
            parse_cell("=A1 + B2 -")
        with self.assertRaises(ValueError):
            parse_cell("A1 + 5")

if __name__ == "__main__":
    unittest.main()