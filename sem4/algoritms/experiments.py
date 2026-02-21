from __future__ import annotations

import random
import string
from dataclasses import dataclass

from algorithms import (
    boyer_moore_horspool_search,
    boyer_moore_horspool_with_alphabet,
    formula_1_big_value,
    karp_rabin_search,
    linear_search,
    rolling_hash,
)


@dataclass
class SearchCase:
    text: str
    pattern: str
    has_match: bool


def random_string(length: int, alphabet: str) -> str:
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_case(text_len: int, pattern_len: int, has_match: bool, alphabet: str) -> SearchCase:
    if pattern_len > text_len:
        raise ValueError("pattern_len must be <= text_len")

    text = random_string(text_len, alphabet)

    if has_match:
        pattern = random_string(pattern_len, alphabet)
        start = random.randint(0, text_len - pattern_len)
        text = text[:start] + pattern + text[start + pattern_len :]
        return SearchCase(text=text, pattern=pattern, has_match=True)

    # Generate a pattern that is absent in text.
    for _ in range(2000):
        pattern = random_string(pattern_len, alphabet)
        if pattern not in text:
            return SearchCase(text=text, pattern=pattern, has_match=False)

    # Fallback for rare unlucky random sequences.
    pattern = "#" * pattern_len
    return SearchCase(text=text, pattern=pattern, has_match=False)


def task_1_demo() -> None:
    text = "ababcabcabababd"
    pattern = "ababd"
    result = linear_search(text, pattern)

    print("ЗАДАНИЕ 1")
    print(f"Текст:    {text}")
    print(f"Образец:  {pattern}")
    print(f"Позиции вхождения: {result.positions}")
    print(f"Количество сравнений: {result.comparisons}")
    print()


def task_2_experiment() -> list[SearchCase]:
    print("ЗАДАНИЕ 2")
    random.seed(42)
    alphabet = string.ascii_lowercase

    lengths = [(120, 4), (400, 6), (1200, 8)]
    all_cases: list[SearchCase] = []

    for has_match in (True, False):
        title = "образец есть в тексте" if has_match else "образца нет в тексте"
        print(f"Случаи: {title}")

        for text_len, pattern_len in lengths:
            case = generate_case(text_len, pattern_len, has_match, alphabet)
            all_cases.append(case)

            result = linear_search(case.text, case.pattern)
            max_ops = (text_len - pattern_len + 1) * pattern_len
            min_ops = text_len - pattern_len + 1
            in_bound = min_ops <= result.comparisons <= max_ops

            print(
                f"n={text_len:4d}, m={pattern_len:2d}, "
                f"сравнений={result.comparisons:6d}, "
                f"ожидаемый_диапазон=[{min_ops}, {max_ops}], "
                f"в_пределах={in_bound}"
            )
        print()

    return all_cases


def task_3_demo() -> None:
    text = "ababcabcabababd"
    pattern = "ababd"
    result = boyer_moore_horspool_search(text, pattern)

    print("ЗАДАНИЕ 3")
    print(f"Текст:    {text}")
    print(f"Образец:  {pattern}")
    print(f"Позиции вхождения: {result.positions}")
    print(f"Сравнений: {result.comparisons}, сдвигов: {result.shifts}")
    print()


def task_4_compare(cases: list[SearchCase]) -> None:
    print("ЗАДАНИЕ 4")
    print("Сравнение линейного поиска и Бойера-Мура-Хорспулла")

    for idx, case in enumerate(cases, start=1):
        linear = linear_search(case.text, case.pattern)
        bmh = boyer_moore_horspool_search(case.text, case.pattern)
        label = "есть вхождение" if case.has_match else "нет вхождения"

        better = "БМХ" if bmh.comparisons < linear.comparisons else "Линейный"
        if bmh.comparisons == linear.comparisons:
            better = "Одинаково"

        print(
            f"Случай {idx:2d} ({label}): "
            f"линейный={linear.comparisons:6d}, "
            f"БМХ={bmh.comparisons:6d}, "
            f"лучше={better}"
        )
    print()


def task_5_demo() -> None:
    text = "301234567890123"
    pattern = "5678"
    alphabet = set("0123456789")

    result = boyer_moore_horspool_with_alphabet(text, pattern, alphabet)

    print("ЗАДАНИЕ 5")
    print("БМХ с предопределенным алфавитом как параметром")
    print(f"Алфавит: {''.join(sorted(alphabet))}")
    print(f"Позиции вхождения: {result.positions}")
    print(f"Сравнений: {result.comparisons}, сдвигов: {result.shifts}")
    print()


def task_6_experiment() -> None:
    print("ЗАДАНИЕ 6")
    print("Тест БМХ с ограниченным алфавитом цифр")

    random.seed(100)
    alphabet = "0123456789"
    case = generate_case(text_len=300, pattern_len=5, has_match=True, alphabet=alphabet)

    result = boyer_moore_horspool_with_alphabet(case.text, case.pattern, set(alphabet))

    print(f"Длина текста: {len(case.text)}")
    print(f"Образец: {case.pattern}")
    print(f"Позиции вхождения: {result.positions[:5]}{'...' if len(result.positions) > 5 else ''}")
    print(f"Сравнений: {result.comparisons}, сдвигов: {result.shifts}")
    print()


def task_7_demo() -> None:
    print("ЗАДАНИЕ 7")
    s = "abracadabra"
    m = 5
    value = formula_1_big_value(s, m)
    print(f"Строка S: {s}, m: {m}")
    print(f"Большое целое значение для первых m символов: {value}")
    print()


def task_8_demo() -> None:
    print("ЗАДАНИЕ 8")
    s = "abracadabra"
    m = 4
    k = 101

    h0, value0 = rolling_hash(s, m, 0, k, 0)
    h1, value1 = rolling_hash(s, m, 1, k, value0)

    print(f"Строка S: {s}, m: {m}, k: {k}")
    print(f"позиция=0 -> хэш={h0}, значение={value0}")
    print(f"позиция=1 -> хэш={h1}, значение={value1}")
    print()


def task_9_demo() -> None:
    print("ЗАДАНИЕ 9")
    text = "ababcabcabababd"
    pattern = "ababd"

    result = karp_rabin_search(text, pattern, k=997)

    print(f"Текст:    {text}")
    print(f"Образец:  {pattern}")
    print(f"Позиции вхождения: {result.positions}")
    print(
        f"Сравнений хэшей: {result.hash_comparisons}, "
        f"Символьных сравнений: {result.char_comparisons}"
    )
    print()


def task_10_experiment() -> None:
    print("ЗАДАНИЕ 10")
    print("Тесты Карпа-Рабина для разных размеров текста и образца")

    random.seed(77)
    alphabet = string.ascii_lowercase
    configs = [
        (200, 5, True),
        (200, 5, False),
        (1000, 8, True),
        (1000, 8, False),
        (3000, 12, True),
        (3000, 12, False),
    ]

    for text_len, pattern_len, has_match in configs:
        case = generate_case(text_len, pattern_len, has_match, alphabet)
        result = karp_rabin_search(case.text, case.pattern, k=1_000_003)
        label = "есть вхождение" if has_match else "нет вхождения"

        print(
            f"n={text_len:4d}, m={pattern_len:2d}, {label:13s}, "
            f"сравнений_хэшей={result.hash_comparisons:5d}, "
            f"сравнений_символов={result.char_comparisons:5d}, "
            f"найдено={len(result.positions)}"
        )
    print()


def run_all_tasks() -> None:
    task_1_demo()
    cases = task_2_experiment()
    task_3_demo()
    task_4_compare(cases)
    task_5_demo()
    task_6_experiment()
    task_7_demo()
    task_8_demo()
    task_9_demo()
    task_10_experiment()
