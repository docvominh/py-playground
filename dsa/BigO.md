# Big O notation

Big O describes how an algorithm's work or extra memory grows as its input grows.
It helps us compare algorithms without depending on a particular computer's speed.

For a list, **n usually means the number of elements**. Big O does not tell us the
exact number of seconds an algorithm will take.

## Common growth rates

| Notation | Name | Example | Effect of doubling n |
| --- | --- | --- | --- |
| O(1) | Constant | Access a list element by index | About the same work |
| O(log n) | Logarithmic | Binary search in a sorted list | About one extra search step |
| O(n) | Linear | Visit every list element once | About twice the work |
| O(n log n) | Linearithmic | Merge sort | A little more than twice the work |
| O(n²) | Quadratic | Bubble sort, average and worst cases | About four times the work |
| O(2ⁿ) | Exponential | Enumerate all subsets of n items | Work roughly squares |

These comparisons describe growth for large inputs, rather than exact operation counts.
For O(2ⁿ), adding just **one** input item already doubles the number of possibilities.

## O(1): constant time

```python
first = values[0]
```

For a nonempty Python list, accessing an element by index takes constant time.
It does not require visiting all the elements, whether the list has 10 or 10,000 items.

## O(n): linear time

```python
for value in values:
    print(value)
```

The loop visits n elements. If the list doubles in size, the number of visits doubles.
Here we treat the work in each iteration as constant; real output cost can also depend
on the size of the value being printed.

## O(log n): logarithmic time

Binary search repeatedly halves the remaining search area in a **sorted** list.

For 16 elements, the search area shrinks like this:

```text
16 → 8 → 4 → 2 → 1
```

Doubling the list size adds about one more halving step. This is why binary search
scales much better than checking every element in sequence.

## Your bubble sort: O(n²) time

```python
for i in range(len(input_array)):
    for j in range(len(input_array) - i - 1):
        if input_array[j] > input_array[j + 1]:
            input_array[j], input_array[j + 1] = (
                input_array[j + 1], input_array[j]
            )
```

The outer loop runs n times. The inner loop gets shorter after each pass:

```text
Pass 1: n - 1 comparisons
Pass 2: n - 2 comparisons
...
Last pass: 0 comparisons
```

The total is:

```text
(n - 1) + (n - 2) + ... + 1 = n(n - 1) / 2
                               = (n² - n) / 2
```

Big O drops constant factors and lower-order terms, so this becomes **O(n²)**.
The n² term dominates as n grows.

| List size | Comparisons |
| --- | --- |
| 10 | 45 |
| 100 | 4,950 |
| 1,000 | 499,500 |

Two nested loops are not automatically O(n²): check how many times each loop
actually runs. These loops produce quadratic growth because their total work is
the sum shown above.

## Best, average, and worst cases

Big O is an upper bound on growth. It does **not** automatically mean worst case;
we should say which case we are analyzing. For a tight bound, the more precise
mathematical notation is Θ (Theta), though O is commonly used in discussions.

Your current bubble sort always performs the comparisons above, even when the
input is already sorted. Its running time is quadratic in the best, average,
and worst cases, assuming constant-time comparisons and swaps.

If you add a `swapped` flag and stop after a pass with no swaps:

- **Best case: O(n)** — an already sorted list needs only one pass.
- **Average case: O(n²)** — many passes are usually needed.
- **Worst case: O(n²)** — a reverse-sorted list needs all the sorting passes.

## Space complexity

Time complexity measures how the amount of work grows.
Space complexity measures how memory use grows.

Your bubble sort modifies the original list and uses only a fixed number of
loop variables and temporary values. Its **auxiliary space complexity is O(1)**.
Auxiliary space means extra memory beyond the input itself.

Python's swap syntax does not change this:

```python
a, b = b, a
```

It preserves only a fixed number of values, regardless of the list size.

By comparison, copying all the elements requires **O(n) extra space**:

```python
copied_values = values.copy()
```

## Rules for simplifying complexity

1. **Drop constant factors:** O(2n) becomes O(n).
2. **Keep the fastest-growing term:** O(n² + n) becomes O(n²).
3. **Add sequential work:** two separate loops over n items take O(n + n) = O(n).
4. **Count nested work:** n outer iterations with n inner iterations take O(n²).
5. **Name independent input sizes:** visiting every pair from lists of sizes n
   and m takes O(n × m), not necessarily O(n²).

A useful question when reading code is: **If the input doubles, how much more
work or extra memory will this code need?**
