from pathlib import Path
from functools import partial
from subprocess import run, DEVNULL
from tqdm import tqdm
from .music_theory import (
    have_opposite_accidentals,
    CHROMATIC_NOTES,
    interval_between,
    harmonic_distance_between,
    NUMBER_OF_CHROMATIC_NOTES,
)

CARDS_DIRECTORY_PATH = "cards/dyad_scores"
CARDS_LIMIT = 100


run_command_silently = partial(run, check=True, stdout=DEVNULL, stderr=DEVNULL)


def _flatten(list_):
    return [item for sublist in list_ for item in sublist]


def _generate_saxophone_notes():
    return _flatten(
        [
            ["as", "bf", "b"],
            (f"{note}'" for note in CHROMATIC_NOTES),
            (f"{note}''" for note in CHROMATIC_NOTES),
            (f"{note}'''" for note in CHROMATIC_NOTES),
        ]
    )


def _generate_all_saxophone_dyads():
    return [
        [first_note, second_note]
        for first_note in _generate_saxophone_notes()
        for second_note in _generate_saxophone_notes()
        if not have_opposite_accidentals(first_note, second_note)
    ]


def _generate_ascending_dyads_on_2_octaves():
    return [
        (first_note, second_note)
        for first_note, second_note in _generate_all_saxophone_dyads()
        if abs(harmonic_distance_between(first_note, second_note))
        < NUMBER_OF_CHROMATIC_NOTES * 2
        and not interval_between(first_note, second_note).startswith("-")
    ]


def generate_lilypond_content(first_note, second_note):
    """
    The content to change all the colors come from this address:
    https://lsr.di.unimi.it/LSR/Search?q=setting+a+color
    """
    return rf"""
        #(define (override-color-for-all-grobs color)
            (lambda (context)
                (let loop ((x all-grob-descriptions))
                    (if (not (null? x))
                        (let ((grob-name (caar x)))
                            (ly:context-pushpop-property context grob-name 'color color)
                            (loop (cdr x)))))))

        \include "lilypond-book-preamble.ly" \language "english" {{
            \applyContext #(override-color-for-all-grobs (x11-color 'white))
            \omit Staff.TimeSignature
            {first_note} {second_note}
        }}
        """


def generate_score_filename(first_note, second_note):
    return (
        f"{first_note}{second_note}_{interval_between(first_note, second_note)}.ly"
    ).replace("'", "-")


def _generate_dyad_score(first_note, second_note, lilypond_score_filepath):
    with open(
        lilypond_score_filepath,
        "w",
        encoding="utf8",
    ) as file:
        file.write(generate_lilypond_content(first_note, second_note))


def _clean_lilypond_intermediate_files(lilypond_score_filepath):
    run_command_silently(
        [
            "rm",
            *[
                f"{lilypond_score_filepath.with_suffix('')}{suffix}"
                for suffix in [
                    "-1.eps",
                    "-1.pdf",
                    "-systems.count",
                    "-systems.tex",
                    "-systems.texi",
                ]
            ],
        ]
    )


def _ly2pdf(lilypond_score_filepath):
    run_command_silently(
        [
            "lilypond",
            f"--output={lilypond_score_filepath.parent}",
            lilypond_score_filepath,
        ],
    )
    _clean_lilypond_intermediate_files(lilypond_score_filepath)


def _pdf2svg(lilypond_score_filepath):
    run_command_silently(
        [
            "inkscape",
            "--pdf-poppler",
            "--export-type=svg",
            f"--export-filename={lilypond_score_filepath.with_suffix('.svg')}",
            lilypond_score_filepath.with_suffix(".pdf"),
        ],
    )


def generate_anki_cards_with_images_of_dyads():
    score_directory = Path(CARDS_DIRECTORY_PATH)
    score_directory.mkdir(parents=True, exist_ok=True)
    for first_note, second_note in tqdm(
        _generate_ascending_dyads_on_2_octaves()[:CARDS_LIMIT],
        desc="Creating the dyads",
    ):
        lilypond_score_filepath = score_directory.joinpath(
            generate_score_filename(first_note, second_note)
        )
        _generate_dyad_score(first_note, second_note, lilypond_score_filepath)
        _ly2pdf(lilypond_score_filepath)
        _pdf2svg(lilypond_score_filepath)


if __name__ == "__main__":
    generate_anki_cards_with_images_of_dyads()
