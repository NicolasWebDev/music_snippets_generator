from shutil import copy, copytree
from pytest import mark
from src.interval_generator.generate_anki_cards import (
    _generate_ascending_dyads_on_2_octaves,
    _negate_svgs_in_directory,
    _pdf2svg,
    _negate_svg,
    _flatten,
    _ly2pdf,
    _compare_svg_files,
)


def test_compare_svg_files():
    assert _compare_svg_files(
        "tests/fixtures/svg/asas_P1.svg", "tests/fixtures/svg/asas_P1.svg"
    )
    assert not _compare_svg_files(
        "tests/fixtures/svg/asas_P1.svg", "tests/fixtures/svg/asa--_d15.svg"
    )
    assert _compare_svg_files(
        "tests/fixtures/asas_P1_negated.svg",
        "tests/fixtures/asas_P1_negated_copy.svg",
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

    assert _compare_svg_files(
        tmp_path / "asas_P1.svg", "tests/fixtures/svg/asas_P1.svg"
    )


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


def test_negate_svgs_in_directory(tmp_path):
    copytree("tests/fixtures/svg", tmp_path, dirs_exist_ok=True)

    _negate_svgs_in_directory(tmp_path)

    assert _compare_svg_files(
        tmp_path / "asas_P1.svg", "tests/fixtures/asas_P1_negated.svg"
    )
    assert _compare_svg_files(
        tmp_path / "asa--_d15.svg", "tests/fixtures/asa--_d15_negated.svg"
    )


def test_negate_svg(tmp_path):
    copy("tests/fixtures/svg/asas_P1.svg", tmp_path / "asas_P1_negated.svg")

    _negate_svg(tmp_path / "asas_P1_negated.svg")

    assert _compare_svg_files(
        tmp_path / "asas_P1_negated.svg", "tests/fixtures/asas_P1_negated.svg"
    )
