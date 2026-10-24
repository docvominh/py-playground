import pytest


def quick_sort(input_array: list[int], low: int = 0, high: int | None = None) -> None:
    """Sort the inclusive range [low, high] in place in ascending order.

    With the default bounds, sort the entire list. Return None.
    For a nonempty range, callers must supply valid list indices.

    Lomuto partitioning chooses the last element as the pivot, places it
    in its final position, then recursively sorts the ranges on either side.
    The algorithm is not stable: equal elements can change relative order.

    For n elements, average time is O(n log n); worst-case time is O(n**2).
    Sorted, reverse-sorted, and all-equal inputs produce worst-case partitions
    with this pivot choice. Partitioning uses O(1) extra space; recursion uses
    O(log n) space on average and O(n) in the worst case, which can exceed
    Python's recursion limit for large inputs.
    """
    if high is None:
        high = len(input_array) - 1

    if low < high:
        pivot_index = __partition(input_array, low, high)
        quick_sort(input_array, low, pivot_index - 1)
        quick_sort(input_array, pivot_index + 1, high)


def __partition(input_array: list[int], low: int, high: int) -> int:
    """Partition [low, high] around its final element and return its new index.

    After partitioning, values to the left are <= the pivot and values to
    the right are > the pivot. Runs in O(high - low + 1) time and O(1) space.
    """
    pivot = input_array[high]

    i = low - 1

    # Grow the <= pivot region; i marks its last index.
    for j in range(low, high):
        if input_array[j] <= pivot:
            i += 1
            input_array[i], input_array[j] = input_array[j], input_array[i]

    # Place the pivot between the <= pivot and > pivot regions.
    input_array[i + 1], input_array[high] = input_array[high], input_array[i + 1]

    return i + 1


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
    quick_sort(input_array, 0, None)

    # Assert
    assert input_array == expected
