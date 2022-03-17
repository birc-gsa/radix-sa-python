"""Radix sorting module."""

from collections import Counter, defaultdict


def count_sort(x: str) -> str:
    """Count-sort the string x.

    >>> count_sort('abaab')
    'aaabb'
    """
    counts = Counter(x)
    return "".join(a * counts[a] for a in sorted(counts))


def bucket_sort(x: str, idx: list[int]) -> list[int]:
    """Bucket-sort the indices in idx using keys from the string x.

    Must have len(x) == len(idx).

    >>> bucket_sort('abaab', [0, 1, 2, 3, 4])
    [0, 2, 3, 1, 4]
    >>> bucket_sort('abaab', [4, 3, 2, 1, 0])
    [3, 2, 0, 4, 1]
    """
    counts = Counter(x)

    buckets = {}
    count = 0
    for a in sorted(counts):
        buckets[a] = count
        count += counts[a]

    out = [0] * len(idx)
    for i in idx:
        a = x[i]
        out[buckets[a]] = i
        buckets[a] += 1

    return out


def key(x: str, suf: int, col: int) -> int:
    """Compute the key for suffix x[suf:] for column col."""
    return ord(x[suf+col]) if suf+col < len(x) else 0


def b_sort(x: str, sufs: list[int], col: int) -> list[int]:
    """Bucket-sort the indices in idx using keys from the string x."""
    counts: dict[int, int] = defaultdict(lambda: 0)
    for i in sufs:
        counts[key(x, i, col)] += 1

    buckets = {}
    count = 0
    for a in sorted(counts):
        buckets[a] = count
        count += counts[a]

    out = [0] * len(sufs)
    for i in sufs:
        a = key(x, i, col)
        out[buckets[a]] = i
        buckets[a] += 1

    return out


def lsd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a least-significant digit radix sort.

    >>> lsd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> lsd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    sufs = list(range(len(x)+1))
    for col in reversed(range(len(sufs))):
        sufs = b_sort(x, sufs, col)
    return sufs


def b_sort_range(
        x: str, sufs: list[int],
        s: list[tuple[int, int, int]]
) -> None:
    """Bucket sort the range sufs[i:j].

    Gets range i:j and column col from the stack in s. Then sorts sufs[i:j]
    and pushes intervals that aren't done yet unto the stack.
    """
    i, j, col = s.pop()

    counts: dict[int, int] = defaultdict(lambda: 0)
    for suf in sufs[i:j]:
        counts[key(x, suf, col)] += 1

    buckets = {}
    count = 0
    for a in sorted(counts):
        buckets[a] = count
        count += counts[a]

    # intervals to be sorted later...
    breakpoints = [i + off for off in buckets.values()] + [j]
    for start, end in zip(breakpoints[:-1], breakpoints[1:]):
        if start + 1 < end:
            s.append((start, end, col + 1))

    # sort the interval
    out = [0] * (j - i)
    for suf in sufs[i:j]:
        a = key(x, suf, col)
        out[buckets[a]] = suf
        buckets[a] += 1

    sufs[i:j] = out


def msd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a most-significant digit radix sort.

    >>> msd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> msd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    sufs = list(range(len(x) + 1))
    s = [(0, len(sufs), 0)]
    while s:
        b_sort_range(x, sufs, s)
    return sufs
