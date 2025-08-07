import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simple_spreadsheet import read_spreadsheet


def test_valid_spreadsheet():
    spreadsheet = [
        ["=B2+5", "=A1-3.5"],
        ["=A1", "42"],
        ["3.14", "=B2"]
    ]
    expected = [
        [47.0, 43.5],
        [47.0, 42.0],
        [3.14, 42.0]
    ]
    assert read_spreadsheet(spreadsheet) == expected


def test_empty_spreadsheet():
    spreadsheet = []
    with pytest.raises(ValueError):
        read_spreadsheet(spreadsheet)


def test_single_cell_spreadsheet():
    spreadsheet = [["42"]]
    assert read_spreadsheet(spreadsheet) == [[42.0]]


@pytest.mark.parametrize("spreadsheet, expected", [
    ([[""]], [[0.0]]),
    ([["3.14", ""], ["", "=A1"]], [[3.14, 0.0], [0.0, 3.14]]),
])
def test_empty_string_cell(spreadsheet, expected):
    assert read_spreadsheet(spreadsheet) == expected


@pytest.mark.parametrize("spreadsheet", [
    [
        ["=B2+5", "=A1-3.5"],
        ["=A1", "42"],
        ["3.14", "=B2"],
        ["=A1+5", "A3"]
    ],
    [
        ["=B2+5", "=A1-3.5"],
        ["=A1", "42"],
        ["3.14", "=B2"],
        ["=A1+5"]
    ],
])
def test_invalid_spreadsheet(spreadsheet):
    with pytest.raises(ValueError):
        read_spreadsheet(spreadsheet)