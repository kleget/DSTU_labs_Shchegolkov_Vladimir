import argparse
import sys
from collections import Counter
from itertools import accumulate
from statistics import median, multimode, pvariance, stdev, variance


DEFAULT_DATA = [17,18,16,16,17,18,19,17,15,17,19,18,16,16,18,18,12,17,15,15,]


def build_series(data):
    if not data:
        raise ValueError("Выборка пуста")

    n = len(data)
    freq = Counter(data)
    xi = sorted(freq.keys())

    ni = []
    for x in xi:
        ni.append(freq[x])

    pi = []
    for count in ni:
        pi.append(count / n)

    Ni = list(accumulate(ni))

    Fi = []
    for c in Ni:
        Fi.append(c / n)

    rows = []
    for i in range(len(xi)):
        rows.append([xi[i], ni[i], pi[i], Ni[i], Fi[i]])
    return rows


def print_differential_series(rows):
    print("Дифференциальный ряд:")
    print("xi\tni\tpi")
    for row in rows:
        print(f"{row[0]:g}\t{row[1]}\t{row[2]:.4f}")
    print()


def print_integral_series(rows):
    print("Интегральный ряд:")
    print("xi\tNi\tFi")
    for row in rows:
        print(f"{row[0]:g}\t{row[3]}\t{row[4]:.4f}")
    print()


def print_main_stats(data, rows):
    sorted_data = sorted(data)
    mean_raw = sum(data) / len(data)

    weighted_sum = 0
    for row in rows:
        weighted_sum += row[0] * row[1]
    mean_grouped = weighted_sum / len(data)

    var_sample = pvariance(data)
    var_corrected = variance(data)
    std_corrected = stdev(data)
    modes = multimode(data)
    value_range = max(data) - min(data)

    print("Основные характеристики выборки:")
    print(f"n = {len(data)}")
    print(f"вариационный ряд = {sorted_data}")
    print(f"размах = {value_range:g}")
    print(f"мода(ы) = {modes}")
    print(f"медиана = {median(data):g}")
    print(f"среднее (по исходной выборке) = {mean_raw:.4f}")
    print(f"среднее (по дифференциальному ряду) = {mean_grouped:.4f}")
    print(f"выборочная дисперсия D = {var_sample:.4f}")
    print(f"исправленная дисперсия S^2 = {var_corrected:.4f}")
    print(f"исправленное СКО s = {std_corrected:.4f}")

    if mean_raw != 0:
        variation_coef = (std_corrected / mean_raw) * 100
        print(f"коэффициент вариации V = {variation_coef:.2f}%")
    print()


def parse_data(raw):
    if raw is None:
        return list(DEFAULT_DATA)

    values = [token.strip() for token in raw.split(",") if token.strip()]
    if not values:
        raise ValueError("Строка с данными пуста")

    numbers = []
    for value in values:
        numbers.append(float(value))
    return numbers


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Лабораторная работа 1, часть 2: единая программа с "
            "дифференциальным и интегральным рядами."
        )
    )
    parser.add_argument(
        "--mode",
        choices=("дифференциальный", "интегральный", "оба"),
        default="оба",
        help="Какой ряд вывести.",
    )
    parser.add_argument(
        "--data",
        help='Значения выборки через запятую. Пример: "1,2,2,3,5"',
    )
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = parse_args()
    data = parse_data(args.data)
    rows = build_series(data)

    print_main_stats(data, rows)

    if args.mode in ("дифференциальный", "оба"):
        print_differential_series(rows)

    if args.mode in ("интегральный", "оба"):
        print_integral_series(rows)


if __name__ == "__main__":
    main()
