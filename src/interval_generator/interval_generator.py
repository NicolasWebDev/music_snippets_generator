from operator import neg, pos
from re import match, search

NUMBER_OF_DIATONIC_NOTES = 7
NUMBER_OF_CHROMATIC_NOTES = 12
DIATONIC_NOTES = ["c", "d", "e", "f", "g", "a", "b"]
DIATONIC_TO_CHROMATIC_NUMBER = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
INTERVALS = {
    0: "P1 d2",
    1: "m2 A1",
    2: "M2 d3",
    3: "m3 A2",
    4: "M3 d4",
    5: "P4 A3",
    6: "d5 A4",
    7: "P5 d6",
    8: "m6 A5",
    9: "M6 d7",
    10: "m7 A6",
    11: "M7 d8",
    12: "P8 A7",
}


def is_flat(note):
    return bool(match(r"^.f$", note))


def is_sharp(note):
    return bool(match(r"^.s$", note))


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
    diatonic_distance = interval_number_from_c4(note)
    harmonic_distance = DIATONIC_TO_CHROMATIC_NUMBER[
        diatonic_distance % NUMBER_OF_DIATONIC_NOTES
    ]
    if diatonic_distance > NUMBER_OF_DIATONIC_NOTES:
        harmonic_distance += (
            (diatonic_distance - 1)
            // NUMBER_OF_DIATONIC_NOTES
            * NUMBER_OF_CHROMATIC_NOTES
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


def interval_between(note1, note2):
    interval_number = interval_number_between(note1, note2)
    is_descending_interval = harmonic_distance_between(note1, note2) < 0
    possible_intervals = INTERVALS[
        abs(harmonic_distance_between(note1, note2)) % NUMBER_OF_CHROMATIC_NOTES
    ]
    quality = search(
        f"(.{str(abs(interval_number) % NUMBER_OF_DIATONIC_NOTES)})",
        possible_intervals,
    )[0][0]
    return f"{'-' if is_descending_interval else ''}{quality}{abs(interval_number)}"
