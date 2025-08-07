import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simple_spreadsheet import read_cell


@pytest.fixture
def sample_spreadsheet():
    return [
        ["=B2+5", "=A1-3.5"],
        ["=A1", "42"],
        ["3.14", "=B2"]
    ]


@pytest.fixture
def circular_spreadsheet():
    return [
        ["=B1+4", "=A2-2"],
        ["=B2-B1", "=A1"]
    ]


@pytest.mark.parametrize("cell_content, expected", [
    ("3.14", 3.14),
    ("42", 42.0),
])
def test_read_number(cell_content, expected, sample_spreadsheet):
    assert read_cell(cell_content, sample_spreadsheet) == expected


@pytest.mark.parametrize("cell_content, expected", [
    ("=A1", 47.0),
    ("=B2", 42.0),
])
def test_read_single_reference(cell_content, expected, sample_spreadsheet):
    assert read_cell(cell_content, sample_spreadsheet) == expected


def test_read_empty_cell(sample_spreadsheet):
    assert read_cell("", sample_spreadsheet) == 0.0


@pytest.mark.parametrize("cell_content", [
    "=X3",
    "=A0",
    "=B-1",
    "=B6",
])
def test_read_invalid_reference(cell_content, sample_spreadsheet):
    with pytest.raises(ValueError):
        read_cell(cell_content, sample_spreadsheet)


@pytest.mark.parametrize("cell_content, expected", [
    ("=A1-3.5", 43.5),
    ("=B2+5", 47.0),
    ("=2.5+B2", 44.5),
    ("=A1-B2", 5.0),
    ("=5+5", 10.0),
])
def test_read_expression(cell_content, expected, sample_spreadsheet):
    assert read_cell(cell_content, sample_spreadsheet) == expected


@pytest.mark.parametrize("cell_content", [
    "=A1",
    "=B1",
    "=A2",
    "=B2",
])
def test_circular_reference(cell_content, circular_spreadsheet):
    with pytest.raises(ValueError):
        read_cell(cell_content, circular_spreadsheet)


@pytest.mark.parametrize("cell_content", [
    "invalid",
    "=A1 +",
    "= + 5",
])
def test_invalid_input(cell_content, sample_spreadsheet):
    with pytest.raises(ValueError):
        read_cell(cell_content, sample_spreadsheet)