from shutil import copy
from filecmp import cmp
from src.music_snippets_generator.music_snippets_generator import (
    _generate_ascending_dyads_on_2_octaves,
    _pdf2svg,
    _ly2pdf,
)


def test_ly2pdf(tmp_path):
    copy("tests/fixtures/asas_P1.ly", tmp_path)

    _ly2pdf(tmp_path / "asas_P1.ly")

    # Can't compare that the pdf created is the same than a fixture, because
    # the ModifyDate is always different.
    assert (tmp_path / "asas_P1.pdf").is_file()
    for file_should_be_deleted in [
        "asas_P1-1.eps",
        "asas_P1-1.pdf",
        "asas_P1-systems.count",
        "asas_P1-systems.texi",
        "asas_P1-systems.tex",
    ]:
        assert not (tmp_path / file_should_be_deleted).is_file()
    assert len(list(tmp_path.iterdir())) == 2


def test_pdf2svg(tmp_path):
    copy("tests/fixtures/asas_P1.pdf", tmp_path)

    _pdf2svg(tmp_path / "asas_P1.pdf")

    assert cmp(tmp_path / "asas_P1.svg", "tests/fixtures/svg/asas_P1.svg")


def test_generate_ascending_dyads_on_2_octaves():
    assert len(_generate_ascending_dyads_on_2_octaves()) == 1494
