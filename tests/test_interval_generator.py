import pytest
from src.interval_generator.note import is_flat, is_sharp


@pytest.mark.parametrize(
    "test_input,expected",
    [("ab", True), ("a", False), ("b", False), ("bb", True), ("bs", False)],
)
def test_is_flat(test_input, expected):
    assert is_flat(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [("ab", False), ("a", False), ("b", False), ("bb", False), ("bs", True)],
)
def test_is_sharp(test_input, expected):
    assert is_sharp(test_input) == expected
