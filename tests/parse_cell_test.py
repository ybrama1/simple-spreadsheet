import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simple_spreadsheet import parse_cell


@pytest.mark.parametrize("cell_content, expected", [
    ("42", (None, None, 42.0)),
    ("3.14", (None, None, 3.14)),
])
def test_parse_number(cell_content, expected):
    assert parse_cell(cell_content) == expected


@pytest.mark.parametrize("cell_content, expected", [
    ("=A1", ("A1", None, None)),
    ("=B2", ("B2", None, None)),
])
def test_parse_single_reference(cell_content, expected):
    assert parse_cell(cell_content) == expected


@pytest.mark.parametrize("cell_content, expected", [
    ("=A1+5", ("A1", "+", 5.0)),
    ("=B2-3.5", ("B2", "-", 3.5)),
    ("=2.5+C3", (2.5, "+", "C3")),
    ("=A1-B2", ("A1", "-", "B2")),
])
def test_parse_expression(cell_content, expected):
    assert parse_cell(cell_content) == expected


def test_empty_cell():
    assert parse_cell("") == (None, None, 0)


@pytest.mark.parametrize("cell_content", [
    "invalid",
    "=A1 +",
    "= + 5",
    "=A1 + B2 + 3",
    "=A1 + B2 -",
    "A1 + 5",
])
def test_invalid_input(cell_content):
    with pytest.raises(ValueError):
        parse_cell(cell_content)