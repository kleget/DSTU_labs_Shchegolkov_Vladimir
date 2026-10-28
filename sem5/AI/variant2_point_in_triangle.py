"""Вариант 2. Проверка принадлежности точки D треугольнику ABC.

Запуск:
    python variant2_point_in_triangle.py

Введите координаты точек A, B, C и D по одной точке на строку.
Формат каждой строки: x y (например: 0 4).
Допускаются целые и вещественные координаты.
"""

import math
import sys
from typing import Tuple

Point = Tuple[float, float]
EPS = 1e-9


def read_point(name: str) -> Point:
    """Считывает и проверяет координаты одной точки."""
    raw = input("Введите координаты точки {} (x y): ".format(name)).strip().split()
    if len(raw) != 2:
        raise ValueError("нужно ввести ровно два числа: x y")

    try:
        x, y = map(float, raw)
    except ValueError as exc:
        raise ValueError("координаты должны быть числами") from exc

    if not (math.isfinite(x) and math.isfinite(y)):
        raise ValueError("координаты должны быть конечными числами")

    return x, y1


def cross_product(p: Point, q: Point, r: Point) -> float:
    """Вычисляет ориентированное векторное произведение для точек P, Q, R."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def orientation_sign(p: Point, q: Point, r: Point) -> int:
    """Возвращает знак ориентации: 1, -1 или 0 с учётом допуска EPS."""
    term1 = (q[0] - p[0]) * (r[1] - p[1])
    term2 = (q[1] - p[1]) * (r[0] - p[0])
    value = cross_product(p, q, r)
    tolerance = EPS * max(1.0, abs(term1), abs(term2))

    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def classify_point(a: Point, b: Point, c: Point, d: Point) -> str:
    """Классифицирует D как inside, boundary или outside.

    Если точки A, B и C лежат на одной прямой, выбрасывает ValueError.
    """
    triangle_orientation = orientation_sign(a, b, c)
    if triangle_orientation == 0:
        raise ValueError("точки A, B и C не образуют треугольник: вершины коллинеарны")

    edge_signs = (
        orientation_sign(a, b, d),
        orientation_sign(b, c, d),
        orientation_sign(c, a, d),
    )

    if any(sign not in (0, triangle_orientation) for sign in edge_signs):
        return "outside"
    if any(sign == 0 for sign in edge_signs):
        return "boundary"
    return "inside"


def print_result(result: str) -> None:
    """Печатает результат классификации на русском языке."""
    messages = {
        "inside": "Точка D находится строго внутри треугольника ABC.",
        "boundary": "Точка D лежит на границе треугольника ABC.",
        "outside": "Точка D находится вне треугольника ABC.",
    }
    print(messages[result])

    if result in ("inside", "boundary"):
        print("Ответ: точка D принадлежит треугольнику ABC (с учётом границы).")
    else:
        print("Ответ: точка D не принадлежит треугольнику ABC.")


def main() -> int:
    print("Проверка принадлежности точки D треугольнику ABC")
    print("Введите координаты каждой точки в формате: x y\n")

    try:
        a = read_point("A")
        b = read_point("B")
        c = read_point("C")
        d = read_point("D")
        result = classify_point(a, b, c, d)
    except (ValueError, EOFError) as exc:
        print("Ошибка: {}".format(exc), file=sys.stderr)
        return 1

    print()
    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
