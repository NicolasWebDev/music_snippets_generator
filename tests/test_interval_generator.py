from pytest import mark
from src.interval_generator.note import is_flat, is_sharp, interval_number_from_c4


@mark.parametrize(
    "test_input,expected",
    [("ab", True), ("a", False), ("b", False), ("bb", True), ("bs", False)],
)
def test_is_flat(test_input, expected):
    assert is_flat(test_input) == expected


@mark.parametrize(
    "test_input,expected",
    [("ab", False), ("a", False), ("b", False), ("bb", False), ("bs", True)],
)
def test_is_sharp(test_input, expected):
    assert is_sharp(test_input) == expected


@mark.parametrize(
    "test_input,expected",
    [
        ("c", 1),
        ("d", 2),
        ("ef", 3),
        ("fs", 4),
        ("g", 5),
        ("ab", 6),
        ("bs", 7),
        ("c'", 8),
        ("d'", 9),
        ("fb'", 11),
        ("as'", 13),
        ("c''", 15),
    ],
)
def test_interval_number_from_c4(test_input, expected):
    assert interval_number_from_c4(test_input) == expected
