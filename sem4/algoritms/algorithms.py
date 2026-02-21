from __future__ import annotations

from dataclasses import dataclass

UNICODE_BASE = 1_114_112  # max Unicode code point + 1


@dataclass
class LinearSearchResult:
    positions: list[int]
    comparisons: int


def linear_search(text: str, pattern: str) -> LinearSearchResult:
    """Simple linear search with counting character comparisons."""
    if pattern == "":
        return LinearSearchResult(list(range(len(text) + 1)), 0)

    n = len(text)
    m = len(pattern)

    if m > n:
        return LinearSearchResult([], 0)

    comparisons = 0
    positions: list[int] = []

    for i in range(n - m + 1):
        matched = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                matched = False
                break
        if matched:
            positions.append(i)

    return LinearSearchResult(positions, comparisons)


@dataclass
class BMHSearchResult:
    positions: list[int]
    comparisons: int
    shifts: int


def _build_bmh_shift_table(pattern: str, alphabet: set[str] | None = None) -> dict[str, int]:
    m = len(pattern)
    default_shift = m if m > 0 else 1

    table: dict[str, int] = {}

    if alphabet is not None:
        for ch in alphabet:
            table[ch] = default_shift

    for i in range(m - 1):
        table[pattern[i]] = m - 1 - i

    return table


def boyer_moore_horspool_search(
    text: str,
    pattern: str,
    alphabet: set[str] | None = None,
) -> BMHSearchResult:
    """Boyer-Moore-Horspool with counting character comparisons."""
    if pattern == "":
        return BMHSearchResult(list(range(len(text) + 1)), 0, 0)

    n = len(text)
    m = len(pattern)

    if m > n:
        return BMHSearchResult([], 0, 0)

    if alphabet is not None:
        for ch in pattern:
            if ch not in alphabet:
                raise ValueError(f"Pattern contains symbol outside alphabet: {ch!r}")

    table = _build_bmh_shift_table(pattern, alphabet)

    positions: list[int] = []
    comparisons = 0
    shifts = 0
    i = 0

    while i <= n - m:
        j = m - 1

        while j >= 0:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j -= 1

        if j < 0:
            positions.append(i)

        shift_char = text[i + m - 1]
        shift = table.get(shift_char, m)
        i += shift
        shifts += 1

    return BMHSearchResult(positions, comparisons, shifts)


def boyer_moore_horspool_with_alphabet(
    text: str,
    pattern: str,
    alphabet: set[str],
) -> BMHSearchResult:
    """BMH for a predefined alphabet. All text and pattern symbols must be in it."""
    for ch in text:
        if ch not in alphabet:
            raise ValueError(f"Text contains symbol outside alphabet: {ch!r}")

    return boyer_moore_horspool_search(text, pattern, alphabet)


@dataclass
class RabinKarpResult:
    positions: list[int]
    hash_comparisons: int
    char_comparisons: int


def formula_1_big_value(s: str, m: int, base: int = UNICODE_BASE) -> int:
    """Task 7: compute big integer for first m symbols of s."""
    if m <= 0:
        raise ValueError("m must be > 0")

    if len(s) < m:
        raise ValueError("Length of s must be at least m")

    value = 0
    for i in range(m):
        value = value * base + ord(s[i])

    return value


def rolling_hash(
    s: str,
    m: int,
    pos: int,
    k: int,
    value: int,
    base: int = UNICODE_BASE,
) -> tuple[int, int]:
    """
    Task 8:
    - if pos == 0, compute value using formula_1_big_value;
    - if pos != 0, update value by rolling formula (2);
    returns (value % k, new_value).
    """
    if m <= 0:
        raise ValueError("m must be > 0")

    if k <= 0:
        raise ValueError("k must be > 0")

    if pos < 0:
        raise ValueError("pos must be >= 0")

    if len(s) < pos + m:
        raise ValueError("Length of s must be at least pos + m")

    if pos == 0:
        value = formula_1_big_value(s, m, base)
    else:
        # Si+1 = (Si - left * base^(m-1)) * base + right
        left = ord(s[pos - 1])
        right = ord(s[pos + m - 1])
        high_power = pow(base, m - 1)
        value = (value - left * high_power) * base + right

    return value % k, value


def karp_rabin_search(
    text: str,
    pattern: str,
    k: int = 1_000_003,
    base: int = UNICODE_BASE,
) -> RabinKarpResult:
    """Rabin-Karp search using rolling_hash from task 8."""
    if pattern == "":
        return RabinKarpResult(list(range(len(text) + 1)), 0, 0)

    n = len(text)
    m = len(pattern)

    if m > n:
        return RabinKarpResult([], 0, 0)

    pattern_value = formula_1_big_value(pattern, m, base)
    pattern_hash = pattern_value % k

    current_hash, current_value = rolling_hash(text, m, 0, k, 0, base)

    positions: list[int] = []
    hash_comparisons = 0
    char_comparisons = 0

    for pos in range(n - m + 1):
        hash_comparisons += 1

        if current_hash == pattern_hash:
            matched = True
            for j in range(m):
                char_comparisons += 1
                if text[pos + j] != pattern[j]:
                    matched = False
                    break

            if matched:
                positions.append(pos)

        if pos < n - m:
            current_hash, current_value = rolling_hash(
                text,
                m,
                pos + 1,
                k,
                current_value,
                base,
            )

    return RabinKarpResult(positions, hash_comparisons, char_comparisons)
