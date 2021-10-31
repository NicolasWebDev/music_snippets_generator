from pathlib import Path
import click
from tqdm import tqdm
from .utils import flatten
from .music_to_pdf import generate_dyad_snippet
from .music_theory import (
    have_opposite_accidentals,
    CHROMATIC_NOTES,
    interval_between,
    harmonic_distance_between,
    NUMBER_OF_CHROMATIC_NOTES,
)

CARDS_DIRECTORY_PATH = "cards/dyad_scores"
CARDS_LIMIT = 1000000000000


def _generate_saxophone_notes():
    return flatten(
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


@click.group(help="Creates snippets of common musical constructs.")
def cli():
    pass


@cli.command()
def dyads():
    generate_anki_cards_with_images_of_dyads()


def generate_anki_cards_with_images_of_dyads():
    score_directory = Path(CARDS_DIRECTORY_PATH)
    score_directory.mkdir(parents=True, exist_ok=True)
    for first_note, second_note in tqdm(
        _generate_ascending_dyads_on_2_octaves()[:CARDS_LIMIT],
        desc="Creating the dyads",
    ):
        generate_dyad_snippet(score_directory, first_note, second_note)


def main():
    cli(prog_name="music-snippets-generator")
