from pytest import mark
from src.music_snippets_generator.utils import flatten


@mark.parametrize(
    "test_array,expected",
    [
        ([[1], [2], [3]], [1, 2, 3]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ],
)
def test_flatten(test_array, expected):
    assert flatten(test_array) == expected
