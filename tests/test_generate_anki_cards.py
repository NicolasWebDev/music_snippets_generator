from filecmp import cmp
from pathlib import Path
from shutil import copy
from pytest import mark
from src.interval_generator.generate_anki_cards import (
    _generate_ascending_dyads_on_2_octaves,
    _pdf2svg,
    _flatten,
    _ly2pdf,
)

SCORE_CONTENT = (
    r'\include "lilypond-book-preamble.ly" \language "english"'
    r" { \omit Staff.TimeSignature as as }"
)


def test_ly2pdf(tmp_path):
    lilypond_score_fixture_path = tmp_path / "lilypond_score_fixture.ly"
    lilypond_score_fixture_path.write_text(SCORE_CONTENT)

    _ly2pdf(lilypond_score_fixture_path)

    # Can't compare that the pdf created is the same than a fixture, because
    # the ModifyDate is always different.
    assert lilypond_score_fixture_path.with_suffix(".pdf").is_file()
    for file_should_be_deleted in [
        "lilypond_score_fixture-1.eps",
        "lilypond_score_fixture-1.pdf",
        "lilypond_score_fixture-systems.count",
        "lilypond_score_fixture-systems.texi",
        "lilypond_score_fixture-systems.tex",
    ]:
        assert not lilypond_score_fixture_path.with_name(
            file_should_be_deleted
        ).is_file()
    assert len(list(tmp_path.iterdir())) == 2


def test_pdf2svg(tmp_path):
    copy("tests/fixtures/asas_P1.pdf", tmp_path)

    _pdf2svg(tmp_path / "asas_P1.pdf")

    assert cmp(tmp_path / "asas_P1.svg", "tests/fixtures/asas_P1.svg")


def test_generate_ascending_dyads_on_2_octaves():
    assert len(_generate_ascending_dyads_on_2_octaves()) == 1494


@mark.parametrize(
    "test_array,expected",
    [
        ([[1], [2], [3]], [1, 2, 3]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ],
)
def test_flatten(test_array, expected):
    assert _flatten(test_array) == expected
