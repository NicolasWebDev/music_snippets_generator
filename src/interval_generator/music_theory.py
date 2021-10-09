from operator import neg, pos
from re import match, search

NUMBER_OF_DIATONIC_NOTES = 7
NUMBER_OF_CHROMATIC_NOTES = 12
DIATONIC_NOTES = ["c", "d", "e", "f", "g", "a", "b"]
CHROMATIC_NOTES = [
    "bs",
    "c",
    "cs",
    "df",
    "d",
    "ds",
    "ef",
    "e",
    "ff",
    "es",
    "f",
    "fs",
    "gf",
    "g",
    "gs",
    "af",
    "a",
    "as",
    "bf",
    "b",
    "cf",
]
DIATONIC_TO_CHROMATIC_DISTANCE = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11}
INTERVALS = {
    0: "P1 d2",
    1: "A1 m2",
    2: "M2 d3",
    3: "A2 m3",
    4: "M3 d4",
    5: "A3 P4 dd5",
    6: "A4 d5",
    7: "AA4 P5 d6",
    8: "A5 m6",
    9: "M6 d7",
    10: "A6 m7",
    11: "M7 d8",
    12: "A7 P8",
}


def is_flat(note):
    return bool(match(r"^.f'*$", note))


def is_sharp(note):
    return bool(match(r"^.s'*$", note))


def interval_number_from_c4(note):
    diatonic_height_from_octaves = note.count("'") * len(DIATONIC_NOTES)
    return 1 + DIATONIC_NOTES.index(note[0]) + diatonic_height_from_octaves


def interval_number_between(first_note, second_note):
    sign = (
        pos
        if interval_number_from_c4(first_note) <= interval_number_from_c4(second_note)
        else neg
    )
    return (
        sign(1)
        + interval_number_from_c4(second_note)
        - interval_number_from_c4(first_note)
    )


def harmonic_distance_from_c4(note):
    diatonic_distance = interval_number_from_c4(note) - 1
    harmonic_distance = DIATONIC_TO_CHROMATIC_DISTANCE[
        diatonic_distance % NUMBER_OF_DIATONIC_NOTES
    ]
    if diatonic_distance >= NUMBER_OF_DIATONIC_NOTES:
        harmonic_distance += (
            diatonic_distance // NUMBER_OF_DIATONIC_NOTES * NUMBER_OF_CHROMATIC_NOTES
        )
    if is_sharp(note):
        harmonic_distance += 1
    elif is_flat(note):
        harmonic_distance -= 1
    return harmonic_distance


def harmonic_distance_between(first_note, second_note):
    return harmonic_distance_from_c4(second_note) - harmonic_distance_from_c4(
        first_note
    )


def have_opposite_accidentals(first_note, second_note):
    return (is_flat(first_note) and is_sharp(second_note)) or (
        is_sharp(first_note) and is_flat(second_note)
    )


def interval_between(first_note, second_note):
    interval_number = interval_number_between(first_note, second_note)
    is_descending_interval = harmonic_distance_between(first_note, second_note) < 0
    harmonic_distance = harmonic_distance_between(first_note, second_note)
    simple_interval_number = simplify_interval_number(abs(interval_number))
    index = (
        12
        if harmonic_distance % 12 == 0
        and harmonic_distance != 0
        and simple_interval_number in (7, 8)
        else abs(harmonic_distance) % 12
    )
    possible_intervals = INTERVALS[index]
    if (
        simple_interval_number == 8
        and abs(harmonic_distance) > 12
        and abs(harmonic_distance) % 12 in (0, 1)
        and search(r"[^']+", first_note)[0] != search(r"[^']+", second_note)[0]
    ):
        simple_interval_number = 1
    quality = search(
        f"[PdAmM]+(?={simple_interval_number})",
        possible_intervals,
    )[0]
    return f"{'-' if is_descending_interval else ''}{quality}{abs(interval_number)}"


def simplify_interval_number(interval_number):
    """
    Transforms an interval number to a simple interval, meaning that if the
    interval number is a compound interval number, then transform it to its
    simple interval number equivalent. If the interval number is already
    simple, return it.
    """
    while interval_number > 8:
        interval_number -= 7
    return interval_number
