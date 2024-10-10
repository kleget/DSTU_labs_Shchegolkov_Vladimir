#задание #14
import math


def test(x, y, z): # проверка на существование треугольника
    if (x+y>z) and (x+z>y) and (y+z>x):
        return True
    return False

def main():
    x = int(input('Введите сторону x:'))
    y = int(input('Введите сторону y:'))
    z = int(input('Введите сторону z:'))

    if test(x, y, z) == True:
        p = (x + y + z) /2 # полупериметр
        S = math.sqrt(p*(p-x)*(p-y)*(p-z))
        print('Площадь треугольника равна: ', S)
        main()
    else:
        print("Такой треугольник не возможен.")
        main()

if __name__ == "__main__":
    main()