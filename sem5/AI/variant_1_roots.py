import numpy as np


def input_data():
    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))
    d = float(input("d = "))
    return a, b, c, d


def find_roots(a, b, c, d):
    if a != 0:
        print("Уравнение третьей степени")
        return np.roots([a, b, c, d])

    elif b != 0:
        print("Уравнение второй степени")
        return np.roots([b, c, d])

    elif c != 0:
        print("Уравнение первой степени")
        return [-d / c]

    else:
        return []


def main():
    a, b, c, d = input_data()
    roots = find_roots(a, b, c, d)

    if len(roots) == 0:
        print("Корней нет")
    else:
        print("Корни:")
        for x in roots:
            print(x)


main()
1