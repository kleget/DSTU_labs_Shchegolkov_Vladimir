import argparse
import sys

import numpy as np


DEFAULT_DATA = [
    17, 18, 16, 16, 17, 18, 19, 17, 15, 17,
    19, 18, 16, 16, 18, 18, 12, 17, 15, 15,
]


def pretty_number(x):
    x = float(x)
    if x.is_integer():
        return int(x)
    return x


def build_series(data):
    if data.size == 0:
        raise ValueError("Выборка пуста")

    n = data.size
    xi, ni = np.unique(data, return_counts=True)
    pi = ni / n
    Ni = np.cumsum(ni)
    Fi = Ni / n

    rows = []
    for i in range(xi.size):
        rows.append([float(xi[i]), int(ni[i]), float(pi[i]), int(Ni[i]), float(Fi[i])])
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


def find_modes(data):
    values, counts = np.unique(data, return_counts=True)
    max_count = np.max(counts)
    return values[counts == max_count]


def print_main_stats(data, rows):
    sorted_data = np.sort(data)
    mean_raw = np.mean(data)

    weighted_sum = 0.0
    for row in rows:
        weighted_sum += row[0] * row[1]
    mean_grouped = weighted_sum / data.size

    var_sample = np.var(data, ddof=0)
    var_corrected = np.var(data, ddof=1)
    std_corrected = np.std(data, ddof=1)
    modes = find_modes(data)
    value_range = np.max(data) - np.min(data)
    med = np.median(data)
    sorted_pretty = [pretty_number(x) for x in sorted_data.tolist()]
    modes_pretty = [pretty_number(x) for x in modes.tolist()]
    med_pretty = pretty_number(med)

    print("Основные характеристики выборки:")
    print(f"n = {data.size}")
    print(f"вариационный ряд = {sorted_pretty}")
    print(f"размах = {value_range:g}")
    print(f"мода(ы) = {modes_pretty}")
    print(f"медиана = {med_pretty}")
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
        return np.array(DEFAULT_DATA, dtype=float)

    values = [token.strip() for token in raw.split(",") if token.strip()]
    if not values:
        raise ValueError("Строка с данными пуста")

    return np.array([float(value) for value in values], dtype=float)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Лабораторная работа 1, часть 2: единая программа с "
            "дифференциальным и интегральным рядами на NumPy."
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


def main():
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
