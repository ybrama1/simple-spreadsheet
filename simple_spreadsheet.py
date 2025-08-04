import re
from typing import List, Optional

Spreadsheet = List[List[str]]

def read_spreadsheet(matrix: Spreadsheet) -> List[List[float]]:
    """
    Evaluates all cells in the matrix and returns a matrix of floats.
    """
    pass

def cell_to_index(cell_ref: str) -> List[int]:
    """
    Converts a cell reference like 'B2' into matrix index (row, col).
    """
    pass

def parse_cell(cell: str) -> List[Optional[str], Optional[str], Optional[float]]:
    """
    Parses a cell content:
    - number to float
    - "=A1" to str (single reference)
    - "=A1 + 5" to tuple (ref1, op, value)
    """
    pass



def read_cell(spreadsheet: Spreadsheet, row: int, col: int) -> float:
    """
    Recursively evaluates the value of a cell, using a cache to avoid re-evaluation.
    """
    pass