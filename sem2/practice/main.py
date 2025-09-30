# """
# Используем метод половинного деления для 
# нахождения корней уравнения.
# """

# import math


# def half_interval(a, b):
#     """Метод делит интервал по полам"""
#     return (a + b) / 2


# def get_parametr():
#     """Получить данные от пользователя"""
#     a = int(input("Введите точку a :"))
#     b = int(input("Введите точку b :"))
#     E = float(input("Введите точность E:"))

#     print('a = {a} Тип:{a1}\nb = {b} Тип {b1}\nE = {E} Тип:{E1}'
#       .format(a=a, a1=type(a), b=b, b1=type(b), E=E, E1=type(E))
#       )
#     return a, b, E


# def func(x):
#     """
#     Вычисляем значение функции, в качестве примера
#     2 cos x -7x = 0
#     """
#     return 2 * math.cos(x) - 7 * x


# def start():
#     """
#     Старт программы
#     """
#     a, b, E = get_parametr()
#     counter = 0
#     max_counter = 200

#     while abs(b - a) > E:

#         counter += 1
#         if counter >= max_counter:
#             print('Слишком много шагов')
#             break

#         if abs(b - a) <= E:
#             print('Значение math.abs(b-a) стало меньше чем E')
#             break

#         print('\n\nШаг №{counter}'.format(counter=counter))

#         fa = func(a)
#         c = half_interval(a, b)
#         fc = func(c)
#         if fa * fc >= 0:
#             a = c
#         else:
#             b = c
#         print('fa = {f_a} fc = {f_c} fa * fc = {res}'.format(f_a=fa, f_c=fc, res=fa * fc))
#         print('a = {a} b = {b}'.format(a=a, b=b))


# # Запуск программы
# start()

import math
import matplotlib.pyplot as plt
import numpy as np

def bisection(f, a, b, eps=1e-5, max_iter=1000):
    """
    Реализация метода половинного деления для решения уравнения f(x) = 0.
    
    Параметры:
        f: Функция уравнения.
        a, b: Границы интервала [a, b].
        eps: Требуемая точность (по умолчанию 1e-5).
        max_iter: Максимальное число итераций (по умолчанию 1000).
    
    Возвращает:
        x: Найденный корень.
        f_x: Значение функции в корне.
        n: Количество итераций.
    """
    if f(a) * f(b) > 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала")
    
    n = 0
    while (b - a) > eps and n < max_iter:
        x = (a + b) / 2
        f_x = f(x)
        n += 1
        
        if f_x == 0:
            return x, f_x, n
            
        if f(a) * f_x < 0:
            b = x
        else:
            a = x
    
    x = (a + b) / 2
    f_x = f(x)
    return x, f_x, n

# Уравнение 1: 5*sin(x) = x - 1  →  5*sin(x) - x + 1 = 0
def eq1(x):
    return 5 * math.sin(x) - x + 1

# Уравнение 2: arctg(x-1) + 2*x = 0
def eq2(x):
    return math.atan(x - 1) + 2 * x

# Точность
eps = 1e-5

# Решение уравнения 1 на интервале [-2, 0]
x1, f1, n1 = bisection(eq1, -2, 0, eps)
print(f"Уравнение 1: x = {x1:.6f}, f(x) = {f1:.6e}, итераций: {n1}")

# Решение уравнения 1 на интервале [2.5, 3] (второй корень)
x2, f2, n2 = bisection(eq1, 2.5, 3, eps)
print(f"Уравнение 1 (второй корень): x = {x2:.6f}, f(x) = {f2:.6e}, итераций: {n2}")

# Решение уравнения 2 на интервале [0, 1]
x3, f3, n3 = bisection(eq2, 0, 1, eps)
print(f"Уравнение 2: x = {x3:.6f}, f(x) = {f3:.6e}, итераций: {n3}")

# Визуализация
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# График для уравнения 1
x_vals = np.linspace(-3, 4, 500)
y_vals1 = [eq1(x) for x in x_vals]
axes[0].plot(x_vals, y_vals1, 'b-', label=r'$5\sin(x) - x + 1$')
axes[0].axhline(0, color='k', linewidth=0.5)
axes[0].scatter([x1, x2], [0, 0], c='red', label='Корни')
axes[0].set_title('Уравнение: $5\sin(x) = x - 1$')
axes[0].set_xlabel('x')
axes[0].set_ylabel('f(x)')
axes[0].legend()
axes[0].grid()

# График для уравнения 2
y_vals2 = [eq2(x) for x in x_vals]
axes[1].plot(x_vals, y_vals2, 'g-', label=r'$arctg(x-1) + 2x$')
axes[1].axhline(0, color='k', linewidth=0.5)
axes[1].scatter([x3], [0], c='red', label='Корень')
axes[1].set_title('Уравнение: $arctg(x-1) + 2x = 0$')
axes[1].set_xlabel('x')
axes[1].legend()
axes[1].grid()

plt.tight_layout()
plt.show()