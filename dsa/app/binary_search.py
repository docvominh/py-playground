import pytest

from app.quick_sort import quick_sort


def search(input_array: list[int], value: int) -> int:
    quick_sort(input_array)

    low = 0
    high = len(input_array) - 1

    while low <= high:
        mid = (low + high) // 2

        if input_array[mid] == value:
            return mid
        elif input_array[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return -1


@pytest.mark.parametrize(
    "input_array, value, expected_index",
    [
        ([1, 2, 3], 1, 0),
        ([1, 2, 3], 3, 2),
        ([1, 5, 3, 7, 3, 4, 10, 99, 2], 1, 0),
        ([1, 5, 3, 7, 3, 4, 10, 99, 2], 99, 8),
        ([1, 2, 3, 7, 3, 4, 10, 99, 5], 3, 2),
    ],
)
def test_buble_sort_default_should_sort_by_ascending(
        input_array: list[int],
        value: int,
        expected_index: int):
    # Arrange & Action
    index = search(input_array, value)

    # Assert
    assert index == expected_index
