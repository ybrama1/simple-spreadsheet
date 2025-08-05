# Simple Spreadsheet

A Python implementation of a basic spreadsheet evaluator that processes matrices containing cell references and mathematical expressions.

## Features

- **Cell Reference Evaluation**: Supports cell references like `A1`, `B2`, etc.
- **Mathematical Operations**: Handles addition (`+`) and subtraction (`-`) operations
- **Formula Processing**: Evaluates formulas starting with `=` (e.g., `=A1+5`, `=B2-3.5`)
- **Recursive Evaluation**: Automatically resolves cell dependencies
- **Error Handling**: Validates cell references and handles out-of-bounds errors

## Usage

### Basic Example

```python
from simple_spreadsheet import read_spreadsheet

# Define a spreadsheet matrix
spreadsheet = [
    ["=B2+5", "=A1-3.5"],
    ["=A1", "42"],
    ["3.14", "=B2"]
]

# Evaluate all cells
result = read_spreadsheet(spreadsheet)
print(result)
# Output: [[47.0, 43.5], [47.0, 42.0], [3.14, 42.0]]
```

### Supported Cell Formats

1. **Numbers**: Direct numeric values (integers or floats)
   - Examples: `42`, `3.14`, `100.5`

2. **Cell References**: References to other cells using `=`
   - Examples: `=A1`, `=B2`, `=C3`

3. **Mathematical Expressions**: Cell references with operations
   - Examples: `=A1+5`, `=B2-3.5`, `=B2+A1`, `=5+A2`

## API Reference

### `read_spreadsheet(matrix: Spreadsheet) -> List[List[float]]`

Evaluates all cells in the matrix and returns a matrix of floats.

**Parameters:**
- `matrix`: A 2D list of strings representing the spreadsheet

**Returns:**
- A 2D list of floats with all formulas evaluated

### `cell_to_index(cell_ref: str) -> List[int]`

Converts a cell reference like 'B2' into matrix index (row, col).

**Parameters:**
- `cell_ref`: Cell reference string (e.g., "A1", "B2")

**Returns:**
- List containing [row, col] indices (0-based)

### `parse_cell(cell: str) -> tuple[Optional[str], Optional[str], Optional[str]]`

Parses cell content and returns reference, operator, and value.

**Parameters:**
- `cell`: Cell content string

**Returns:**
- Tuple containing (reference, operator, reference)

### `read_cell(cell: str, spreadsheet: Spreadsheet) -> float`

Recursively evaluates the value of a single cell.

**Parameters:**
- `cell`: Cell content string
- `spreadsheet`: The complete spreadsheet matrix

**Returns:**
- Evaluated numeric value of the cell

## Cell Reference System

- Columns are labeled with letters: A, B, C, ...
- Rows are labeled with numbers: 1, 2, 3, ...
- Cell references combine column letter and row number: A1, B2, C3, etc.
- Internal indexing is 0-based (A1 = [0,0], B2 = [1,1])

## Error Handling

The library handles several error conditions:

- **Invalid cell references**: Non-standard formats throw `ValueError`
- **Out of bounds references**: References to non-existent cells throw `ValueError`
- **Invalid cell content**: Malformed formulas throw `ValueError`

## Testing

The project includes comprehensive unit tests:

```bash
python -m unittest cell_to_index_test.py
python -m unittest parse_cell_test.py
python -m unittest read_cell_test.py
python -m unittest read_spreadsheet_test.py
```

Or run all tests:

```bash
python -m unittest discover -p "*test.py"
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## File Structure

```
simple_spreadsheet/
├── simple_spreadsheet.py      # Main implementation
├── cell_to_index_test.py      # Tests for cell reference conversion
├── parse_cell_test.py         # Tests for cell parsing
├── read_cell_test.py          # Tests for cell evaluation
├── read_spreadsheet_test.py   # Tests for full spreadsheet evaluation
└── README.md                  # This file
```

## Limitations

- Only supports single-letter column names (A-Z, max 26 columns)
- Only supports addition (+) and subtraction (-) operations
- No support for multiplication, division, or complex formulas
- No support for string values or mixed data types