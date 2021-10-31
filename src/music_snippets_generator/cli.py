import click
from .music_snippets_generator import generate_anki_cards_with_images_of_dyads


@click.group(help="Creates snippets of common musical constructs.")
def cli():
    pass


@cli.command()
def dyads():
    generate_anki_cards_with_images_of_dyads()


def main():
    cli(prog_name="music-snippets-generator")
