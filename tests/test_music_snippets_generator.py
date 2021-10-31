from src.music_snippets_generator.music_snippets_generator import (
    _generate_ascending_dyads_on_2_octaves,
)


def test_generate_ascending_dyads_on_2_octaves():
    assert len(_generate_ascending_dyads_on_2_octaves()) == 1494
