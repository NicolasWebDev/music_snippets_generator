from re import match

FIRST_OCTAVE_NON_FLAT_NOTES = "as b".split()
SECOND_OCTAVE_NON_FLAT_NOTES = "c' cs' d' ds' e' f' fs' g' gs' a' as' b'".split()
THIRD_OCTAVE_NON_FLAT_NOTES = (
    "c'' cs'' d'' ds'' e'' f'' fs'' g'' gs'' a'' as'' b''".split()
)
FOURTH_OCTAVE_NON_FLAT_NOTES = "c''' cs''' d''' ds''' e''' f''' fs'''".split()
NON_FLAT_NOTES = (
    FIRST_OCTAVE_NON_FLAT_NOTES
    + SECOND_OCTAVE_NON_FLAT_NOTES
    + THIRD_OCTAVE_NON_FLAT_NOTES
    + FOURTH_OCTAVE_NON_FLAT_NOTES
)

FIRST_OCTAVE_FLAT_NOTES = "bf b".split()
SECOND_OCTAVE_FLAT_NOTES = "c' df' d' ef' e' f' gf' g' af' a' bf' b'".split()
THIRD_OCTAVE_FLAT_NOTES = "c'' df'' d'' ef'' e'' f'' gf'' g'' af'' a'' bf'' b''".split()
FOURTH_OCTAVE_FLAT_NOTES = "c''' df''' d''' ef''' e''' f''' gf'''".split()
FLAT_NOTES = (
    FIRST_OCTAVE_FLAT_NOTES
    + SECOND_OCTAVE_FLAT_NOTES
    + THIRD_OCTAVE_FLAT_NOTES
    + FOURTH_OCTAVE_FLAT_NOTES
)

INTERVALS = "P1 m2 M2 m3 M3 P4 T P5 m6 M6 m7 M7 P8".split()


def is_flat(note):
    return bool(match(r"^.f", note))


def generate_lilypond_content(first_note, second_note):
    return (
        '\\include "lilypond-book-preamble.ly" \\language "english"'
        f" {{ \\omit Staff.TimeSignature {first_note} {second_note} }}"
    )


def generate_file_name(first_note, second_note, interval):
    return f"{first_note}{second_note}_{interval}.ly".replace("'", "-")


def generate_score_file(first_note, second_note, interval):
    with open(
        generate_file_name(first_note, second_note, interval), "w", encoding="utf8"
    ) as file:
        file.write(generate_lilypond_content(first_note, second_note))


def generate_non_flat_score_files(non_flat_notes):
    for i, _ in enumerate(non_flat_notes):
        for j, _ in enumerate(non_flat_notes):
            if (i <= j) and (j - i <= 12):
                first_note = non_flat_notes[i]
                second_note = non_flat_notes[j]
                interval = INTERVALS[j - i]
                generate_score_file(first_note, second_note, interval)


def generate_flat_score_files(flat_notes):
    for i, _ in enumerate(flat_notes):
        for j, _ in enumerate(flat_notes):
            if (i <= j) and (j - i <= 12):
                first_note = flat_notes[i]
                second_note = flat_notes[j]
                if is_flat(first_note) or is_flat(second_note):
                    interval = INTERVALS[j - i]
                    generate_score_file(first_note, second_note, interval)


generate_non_flat_score_files(NON_FLAT_NOTES)
generate_flat_score_files(FLAT_NOTES)
