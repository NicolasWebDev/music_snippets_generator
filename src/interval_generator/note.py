from re import match


def is_flat(note):
    return bool(match(r"^.b$", note))


def is_sharp(note):
    return bool(match(r"^.s$", note))
