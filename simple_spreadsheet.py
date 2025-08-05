import re
from typing import List, Optional

Spreadsheet = List[List[str]]

def read_spreadsheet(matrix: Spreadsheet) -> List[List[float]]:
    """
    Evaluates all cells in the matrix and returns a matrix of floats.
    """
    evaluate_row = lambda row: list(map(lambda cell: read_cell(cell, matrix), row)) # Apply read_cell to each cell in the row

    Spreadsheet = list(map(evaluate_row, matrix)) # Apply evaluate_row to each row in the matrix
    return Spreadsheet

def cell_to_index(cell_ref: str) -> List[int]:
    """
    Converts a cell reference like 'B2' into matrix index (row, col).
    """
    if not re.match(r'^[A-Z][0-9]+$', cell_ref): # Check for valid format, with regular expression
        raise ValueError(f"Invalid cell reference: {cell_ref}")

    col = ord(cell_ref[0]) - ord('A')  # Convert column letter to index (0-based)
    row = int(cell_ref[1:]) - 1
    return [row, col]

def parse_cell(cell: str) -> tuple[Optional[str], Optional[str], Optional[float]]:
    """
    Parses a cell content:
    - number to float
    - "=A1" to str (single reference)
    - "=A1 + 5" to tuple (ref1, op, value)
    """
    if cell == "":
        return (None, None, 0)  # Empty cell

    # Check if the cell is a number
    #regular expression to match a number, which can be an integer or a float.
    float_pattern = r'(\d+(\.\d+)?)'
    reference_pattern = r'([A-Z][0-9]+)'
    if re.match(fr'^{float_pattern}$', cell):
        return (None, None, float(cell))  # It's a number


    #regular expression to match single reference or expression.
    #group1 is the reference, group6 is the operator, and group7 is the second reference.
    match = re.match(fr'^=({reference_pattern}|{float_pattern})(([\+\-])({float_pattern}|{reference_pattern}))?$', cell)
    if match:
        ref1 = match.group(1) if match.group(1) else None  # Reference like 'A1' or a number
        op = match.group(6) if match.group(6) else None  # Operator like '+' or '-'
        ref2 = match.group(7) if match.group(7) else None  # Value or another reference
    else:
        raise ValueError(f"Invalid cell content: {cell}")
    # If ref2 or ref1 is a number, convert it to float
    if ref1 and re.match(fr'^{float_pattern}$', ref1):
        ref1 = float(ref1)
    if ref2 and re.match(fr'^{float_pattern}$', ref2):
        ref2 = float(ref2)
    return (ref1, op, ref2)

def read_cell(cell: str, spreadsheet: Spreadsheet, last_refs = []) -> float:
    """
    Recursively evaluates the value of a cell
    """
    def value_of_ref(ref: str) -> float:
        """
        Returns the value of a cell reference.
        """
        if isinstance(ref, float):  # If ref is already a float, return it directly
            return ref
        if ref in last_refs:
            raise ValueError(f"Circular reference detected: {ref} in {last_refs}")
        row, col = cell_to_index(ref)
        if row < 0 or row >= len(spreadsheet) or col < 0 or col >= len(spreadsheet[0]):
            raise ValueError(f"Cell reference {ref} is out of bounds.")
        return read_cell(spreadsheet[row][col], spreadsheet, last_refs + [ref])  # Recursively read the referenced cell
    ref1, op, ref2 = parse_cell(cell)  # Parse the cell content
    ref1_value = 0
    if ref1:
        ref1_value = value_of_ref(ref1)

    ref2_value = 0
    if ref2:
        ref2_value = value_of_ref(ref2)

    if op == '+':
        return ref1_value + ref2_value
    elif op == '-':
        return ref1_value - ref2_value
    else:
        return ref2_value or ref1_value  # No operation, just return the referenced cell value