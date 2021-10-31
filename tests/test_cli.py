from unittest.mock import patch
from click.testing import CliRunner
from src.music_snippets_generator.cli import cli


def test_cli():
    assert CliRunner().invoke(cli).exit_code == 0


@patch(
    "src.music_snippets_generator.cli.generate_anki_cards_with_images_of_dyads",
)
def test_dyads(mock_function):
    assert CliRunner().invoke(cli, ["dyads"]).exit_code == 0
    mock_function.assert_called_with()
