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
    
    col = ord(cell_ref[0]) - ord('A')
    row = int(cell_ref[1:]) - 1
    return [row, col]

def parse_cell(cell: str) -> tuple[Optional[str], Optional[str], Optional[float]]:
    """
    Parses a cell content:
    - number to float
    - "=A1" to str (single reference)
    - "=A1 + 5" to tuple (ref1, op, value)
    """

    # Check if the cell is a number
    #regular expression to match a number, which can be an integer or a float.
    if re.match(r'^\d+(\.\d+)?$', cell):
        return (None, None, float(cell))


    #regular expression to match single reference or expression.
    #group1 is the reference, group2 is the operator, and group3 is the value.
    match = re.match(r'^=([A-Z]\d+)(([\+\-])(\d+(\.\d+)?))?$', cell)
    if match:
        ref = match.group(1)
        op = match.group(3) if match.group(3) else None
        value = float(match.group(4)) if match.group(4) else None
        return (ref, op, value)
    
    raise ValueError(f"Invalid cell content: {cell}")



def read_cell(cell: str, spreadsheet: Spreadsheet) -> float:
    """
    Recursively evaluates the value of a cell
    """
    ref, op, value = parse_cell(cell)
    
    if ref is None:
        return value  # It's a number
    
    row, col = cell_to_index(ref)
    
    if row < 0 or row >= len(spreadsheet) or col < 0 or col >= len(spreadsheet[0]):
        raise ValueError(f"Cell reference {ref} out of bounds.")
    
    cell_value = read_cell(spreadsheet[row][col], spreadsheet)
    
    if op == '+':
        return cell_value + value
    elif op == '-':
        return cell_value - value
    else:
        return cell_value  # No operation, just return the referenced cell value