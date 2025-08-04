import unittest
from simple_spreadsheet import cell_to_index

class TestCellToIndex(unittest.TestCase):

    def test_valid_references(self):
        self.assertEqual(cell_to_index("A1"), [0, 0])
        self.assertEqual(cell_to_index("B2"), [1, 1])
        self.assertEqual(cell_to_index("C3"), [2, 2])

    def test_invalid_references(self):
        with self.assertRaises(ValueError):
            cell_to_index("0A")
        with self.assertRaises(ValueError):
            cell_to_index("")

if __name__ == "__main__":
    unittest.main()