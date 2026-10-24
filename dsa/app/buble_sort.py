import pytest


def buble_sort(input_array: list[int]) -> list[int]:
    """Sort a list of integers in ascending order using bubble sort.

    Compare neighboring elements and swap them when they are out of order.
    Each pass moves the largest remaining element to the end of the unsorted
    section, so the next pass can skip that element.

    Args:
        input_array: The list of integers to sort. Sorting modifies this list
            in place.

    Returns:
        The sorted input list, or a new empty list if the input is empty.

    Complexity:
        O(n²) time in the best, average, and worst cases because this version
        does not stop early when a pass makes no swaps. Uses O(1) extra space.
    """
    if len(input_array) == 0:
        return []

    if len(input_array) == 1:
        return input_array

    for i in range(len(input_array)):
        for j in range(0, len(input_array) - i - 1):
            if input_array[j + 1] < input_array[j]:
                input_array[j], input_array[j + 1] = input_array[j + 1], input_array[j]

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
def test_buble_sort_default_should_sort_by_ascending(input_array: list[int], expected: list[int]):
    # Arrange & Action
    buble_sort(input_array)

    # Assert
    assert input_array == expected
