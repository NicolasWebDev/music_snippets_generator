from pytest import mark
from src.interval_generator.note import (
    is_flat,
    is_sharp,
    diatonic_distance_from_c4,
    diatonic_distance_between,
    harmonic_distance_from_c4,
)


@mark.parametrize(
    "test_note,expected",
    [("af", True), ("a", False), ("b", False), ("bf", True), ("bs", False)],
)
def test_is_flat(test_note, expected):
    assert is_flat(test_note) == expected


@mark.parametrize(
    "test_note,expected",
    [("af", False), ("a", False), ("b", False), ("bf", False), ("bs", True)],
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
        ("af", 6),
        ("bs", 7),
        ("c'", 8),
        ("d'", 9),
        ("fb'", 11),
        ("as'", 13),
        ("c''", 15),
    ],
)
def test_diatonic_distance_from_c4(test_note, expected):
    assert diatonic_distance_from_c4(test_note) == expected


@mark.parametrize(
    "test_note1,test_note2,expected",
    [
        ("cf", "cs", 1),
        ("c", "c", 1),
        ("c", "c'", 8),
        ("c", "c''", 15),
        ("d", "d", 1),
        ("ef", "c'", 6),
        ("c'", "ef", -6),
        ("d", "c", -2),
    ],
)
def test_diatonic_distance_between(test_note1, test_note2, expected):
    assert diatonic_distance_between(test_note1, test_note2) == expected


@mark.parametrize(
    "test_note,expected",
    [
        ("c", 0),
        ("d", 2),
        ("e", 4),
        ("f", 5),
        ("fs", 6),
        ("ff", 4),
        ("c'", 12),
        ("c'''", 36),
        ("d'''", 38),
    ],
)
def test_harmonic_distance_from_c4(test_note, expected):
    assert harmonic_distance_from_c4(test_note) == expected
