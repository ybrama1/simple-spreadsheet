import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simple_spreadsheet import cell_to_index


@pytest.mark.parametrize("cell_ref, expected", [
    ("A1", [0, 0]),
    ("B2", [1, 1]),
    ("C3", [2, 2]),
])
def test_valid_references(cell_ref, expected):
    assert cell_to_index(cell_ref) == expected


@pytest.mark.parametrize("cell_ref", [
    "0A",
    "",
])
def test_invalid_references(cell_ref):
    with pytest.raises(ValueError):
        cell_to_index(cell_ref)