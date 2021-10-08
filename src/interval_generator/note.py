from operator import neg, pos
from re import match

NUMBER_OF_DIATONIC_NOTES = 7
NUMBER_OF_CHROMATIC_NOTES = 12
DIATONIC_NOTES = ["c", "d", "e", "f", "g", "a", "b"]
DIATONIC_TO_CHROMATIC_NUMBER = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def is_flat(note):
    return bool(match(r"^.f$", note))


def is_sharp(note):
    return bool(match(r"^.s$", note))


def diatonic_distance_from_c4(note):
    diatonic_height_from_octaves = note.count("'") * len(DIATONIC_NOTES)
    return 1 + DIATONIC_NOTES.index(note[0]) + diatonic_height_from_octaves


def diatonic_distance_between(first_note, second_note):
    sign = (
        pos
        if diatonic_distance_from_c4(first_note)
        <= diatonic_distance_from_c4(second_note)
        else neg
    )
    return (
        sign(1)
        + diatonic_distance_from_c4(second_note)
        - diatonic_distance_from_c4(first_note)
    )


def harmonic_distance_from_c4(note):
    diatonic_distance = diatonic_distance_from_c4(note)
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
