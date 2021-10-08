from pytest import mark
from src.interval_generator.note import (
    is_flat,
    is_sharp,
    interval_number_from_c4,
    interval_number_between,
)


@mark.parametrize(
    "test_note,expected",
    [("ab", True), ("a", False), ("b", False), ("bb", True), ("bs", False)],
)
def test_is_flat(test_note, expected):
    assert is_flat(test_note) == expected


@mark.parametrize(
    "test_note,expected",
    [("ab", False), ("a", False), ("b", False), ("bb", False), ("bs", True)],
)
def test_is_sharp(test_note, expected):
    assert is_sharp(test_note) == expected


@mark.parametrize(
    "test_note,expected",
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
def test_interval_number_from_c4(test_note, expected):
    assert interval_number_from_c4(test_note) == expected


@mark.parametrize(
    "test_note1,test_note2,expected",
    [
        ("cb", "cs", 1),
        ("c", "c", 1),
        ("c", "c'", 8),
        ("c", "c''", 15),
        ("d", "d", 1),
        ("ef", "c'", 6),
        ("c'", "ef", -6),
        ("d", "c", -2),
    ],
)
def test_interval_number_between(test_note1, test_note2, expected):
    assert interval_number_between(test_note1, test_note2) == expected
