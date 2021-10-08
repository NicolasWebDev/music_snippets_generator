from re import match

DIATONIC_NOTES = "c d e f g a b".split()


def is_flat(note):
    return bool(match(r"^.b$", note))


def is_sharp(note):
    return bool(match(r"^.s$", note))


def interval_number_from_c4(note):
    diatonic_height_from_octaves = note.count("'") * len(DIATONIC_NOTES)
    return 1 + DIATONIC_NOTES.index(note[0]) + diatonic_height_from_octaves
