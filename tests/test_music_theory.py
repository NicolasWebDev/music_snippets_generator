from pytest import mark
from src.music_snippets_generator.music_theory import (
    _simplify_interval_number,
    have_opposite_accidentals,
    _is_flat,
    _is_sharp,
    _interval_number_from_c4,
    _interval_number_between,
    _harmonic_distance_from_c4,
    harmonic_distance_between,
    interval_between,
)


@mark.parametrize(
    "test_note,expected",
    [
        ("af", True),
        ("a", False),
        ("b", False),
        ("bf", True),
        ("bs", False),
        ("bs'", False),
        ("bf'''", True),
    ],
)
def test_is_flat(test_note, expected):
    assert _is_flat(test_note) == expected


@mark.parametrize(
    "test_note,expected",
    [
        ("af", False),
        ("a", False),
        ("b", False),
        ("bf", False),
        ("bs", True),
        ("bs'", True),
        ("bf'''", False),
    ],
)
def test_is_sharp(test_note, expected):
    assert _is_sharp(test_note) == expected


@mark.parametrize(
    "test_note1,test_note2,expected",
    [
        ("af", "as", True),
        ("af", "a", False),
        ("as", "af", True),
        ("as", "as", False),
        ("af", "af", False),
    ],
)
def test_have_opposite_accidentals(test_note1, test_note2, expected):
    assert have_opposite_accidentals(test_note1, test_note2) == expected


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
def test_interval_number_from_c4(test_note, expected):
    assert _interval_number_from_c4(test_note) == expected


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
def test_interval_number_between(test_note1, test_note2, expected):
    assert _interval_number_between(test_note1, test_note2) == expected


@mark.parametrize(
    "test_note,expected",
    [
        ("c", 0),
        ("d", 2),
        ("e", 4),
        ("f", 5),
        ("fs", 6),
        ("ff", 4),
        ("bf", 10),
        ("c'", 12),
        ("c'''", 36),
        ("d'''", 38),
    ],
)
def test_harmonic_distance_from_c4(test_note, expected):
    assert _harmonic_distance_from_c4(test_note) == expected


@mark.parametrize(
    "test_note1,test_note2,expected",
    [
        ("c", "c", 0),
        ("as", "bf", 0),
        ("c", "d", 2),
        ("d", "d'", 12),
        ("d'", "d", -12),
        ("e", "f", 1),
        ("d", "c", -2),
        ("as", "f'", 7),
        ("as", "fs'", 8),
    ],
)
def test_harmonic_distance_between(test_note1, test_note2, expected):
    assert harmonic_distance_between(test_note1, test_note2) == expected


@mark.parametrize(
    "test_note1,test_note2,expected",
    [
        ("c", "c", "P1"),
        ("c", "d", "M2"),
        ("c", "df", "m2"),
        ("cs", "d", "m2"),
        ("c'", "c''", "P8"),
        ("c", "d'", "M9"),
        ("cf", "d'", "A9"),
        ("d'", "cf", "-A9"),
        ("d", "c", "-M2"),
        ("as", "g'", "d7"),
        ("as", "a'", "d8"),
        ("b", "ff'", "dd5"),
        ("bs'", "f'", "-AA4"),
        ("bf", "b'", "A8"),
        ("bf", "b''", "A15"),
        ("b", "cf''", "d9"),
        ("b''", "bf", "-A15"),
        ("as", "a''", "d15"),
        ("as", "as''", "P15"),
        ("cf'", "b'", "A7"),
        ("cf'", "b''", "A14"),
    ],
)
def test_interval_between(test_note1, test_note2, expected):
    assert interval_between(test_note1, test_note2) == expected


@mark.parametrize(
    "note,expected",
    [(9, 2), (1, 1), (8, 8), (11, 4), (13, 6), (15, 8), (16, 2)],
)
def test_simplify_interval_number(note, expected):
    assert _simplify_interval_number(note) == expected
