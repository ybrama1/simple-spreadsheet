# Simple Spreadsheet

A Python implementation of a basic spreadsheet evaluator that processes matrices containing cell references and mathematical expressions.

## Features

- **Cell Reference Evaluation**: Supports cell references like `A1`, `B2`, etc.
- **Mathematical Operations**: Handles addition (`+`) and subtraction (`-`) operations
- **Formula Processing**: Evaluates formulas starting with `=` (e.g., `=A1+5`, `=B2-3.5`)
- **Recursive Evaluation**: Automatically resolves cell dependencies
- **Error Handling**: Validates cell references and handles out-of-bounds errors

## Usage

### Web Interface

The easiest way to use the spreadsheet is through the web interface:

1. **Start the web server:**
   ```bash
   python app.py
   ```

2. **Open your browser** and go to: `http://127.0.0.1:5000`

3. **Use the interface:**
   - Enter formulas and values in the input spreadsheet
   - Click "Evaluate" to see the results
   - Use "Load Example" to see a sample spreadsheet
   - Resize the spreadsheet using the row/column controls

### Python API

You can also use the functions directly in Python:

#### Basic Example

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

## Web API Endpoints

The web server provides REST API endpoints for programmatic access:

### `POST /api/evaluate`
Evaluates a complete spreadsheet matrix.

**Request Body:**
```json
{
  "matrix": [
    ["=B2+5", "=A1-3.5"],
    ["=A1", "42"],
    ["3.14", "=B2"]
  ]
}
```

**Response:**
```json
{
  "success": true,
  "result": [[47.0, 43.5], [47.0, 42.0], [3.14, 42.0]],
  "original": [["=B2+5", "=A1-3.5"], ["=A1", "42"], ["3.14", "=B2"]]
}
```

### `POST /api/parse_cell`
Parses a single cell formula.

**Request Body:**
```json
{
  "cell": "=A1+5"
}
```

**Response:**
```json
{
  "success": true,
  "ref1": "A1",
  "operator": "+",
  "ref2": 5.0
}
```

### `POST /api/cell_to_index`
Converts cell reference to matrix indices.

**Request Body:**
```json
{
  "cell_ref": "B2"
}
```

**Response:**
```json
{
  "success": true,
  "row": 1,
  "col": 1
}
```

### `POST /api/read_cell`
Evaluates a single cell in context of a spreadsheet.

**Request Body:**
```json
{
  "cell": "=A1+5",
  "matrix": [["42"], ["3.14"]]
}
```

**Response:**
```json
{
  "success": true,
  "result": 47.0
}
```

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

The project uses pytest with parametrized tests for comprehensive coverage. All tests are organized in the `tests/` folder:

```bash
pytest tests/cell_to_index_test.py
pytest tests/parse_cell_test.py
pytest tests/read_cell_test.py
pytest tests/read_spreadsheet_test.py
```

Or run all tests:

```bash
pytest tests/
```

Or simply:

```bash
pytest
```

Run with verbose output:

```bash
pytest tests/ -v
```

## Requirements

- Python 3.6+
- Flask and Flask-CORS for web interface
- pytest for testing
- No other external dependencies (core library uses only standard library)

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## File Structure

```
simple_spreadsheet/
├── simple_spreadsheet.py      # Main implementation
├── app.py                     # Flask web server
├── requirements.txt           # Python dependencies
├── templates/                 # Web interface templates
│   └── index.html            # Main web interface
├── tests/                     # Test directory
│   ├── __init__.py           # Tests package initialization
│   ├── cell_to_index_test.py # Tests for cell reference conversion
│   ├── parse_cell_test.py    # Tests for cell parsing
│   ├── read_cell_test.py     # Tests for cell evaluation
│   └── read_spreadsheet_test.py # Tests for full spreadsheet evaluation
└── README.md                  # This file
```

## Limitations

- Only supports single-letter column names (A-Z, max 26 columns)
- Only supports addition (+) and subtraction (-) operations
- No support for multiplication, division, or complex formulas
- No support for string values or mixed data types