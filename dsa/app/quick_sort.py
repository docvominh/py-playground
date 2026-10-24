import pytest


def quick_sort(input_array: list[int]) -> list[int]:
    return input_array


@pytest.mark.parametrize(
    "input_array, expected",
    [
        ([4, 6, 9, 2, 3, 5], [2, 3, 4, 5, 6, 9]),
        ([], []),
        ([1], [1]),
        ([3, 1, 3], [1, 3, 3]),
        ([3, 2, 1], [1, 2, 3]),
        ([-3, 2, 1], [-3, 1, 2]),
    ],
)
def test_quick_sort_default_should_sort_by_ascending(input_array: list[int], expected: list[int]):
    # Arrange & Action
    quick_sort(input_array)

    # Assert
    assert input_array == expected
