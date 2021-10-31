from functools import partial
from subprocess import run, DEVNULL
from .music_theory import interval_between

run_command_silently = partial(run, check=True, stdout=DEVNULL, stderr=DEVNULL)


def generate_dyad_snippet(score_directory, first_note, second_note):
    lilypond_score_filepath = score_directory.joinpath(
        _generate_score_filename(first_note, second_note)
    )
    _generate_dyad_score(first_note, second_note, lilypond_score_filepath)
    _ly2pdf(lilypond_score_filepath)
    _pdf2svg(lilypond_score_filepath)


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


def _ly2pdf(lilypond_score_filepath):
    run_command_silently(
        [
            "lilypond",
            f"--output={lilypond_score_filepath.parent}",
            lilypond_score_filepath,
        ],
    )
    _clean_lilypond_intermediate_files(lilypond_score_filepath)


def _generate_score_filename(first_note, second_note):
    return (
        f"{first_note}{second_note}_{interval_between(first_note, second_note)}.ly"
    ).replace("'", "-")


def _generate_lilypond_content(first_note, second_note):
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


def _generate_dyad_score(first_note, second_note, lilypond_score_filepath):
    with open(
        lilypond_score_filepath,
        "w",
        encoding="utf8",
    ) as file:
        file.write(_generate_lilypond_content(first_note, second_note))


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
