import math
import matplotlib.pyplot as plt
import numpy as np

def safe_eval(expr):
    """Безопасное преобразование строки в математическую функцию"""
    # Создаем безопасный словарь функций
    safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    safe_dict['x'] = None  # Разрешаем переменную x
    
    # Проверяем имена в выражении
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in safe_dict:
            raise NameError(f"Использование имени '{name}' не разрешено")
    
    # Возвращаем функцию с обработкой ошибок вычислений
    def func(x):
        try:
            return eval(expr, {"__builtins__": None}, {**safe_dict, "x": x})
        except Exception as e:
            raise ValueError(f"Ошибка вычисления при x={x}: {e}")
    
    return func

def bisection(f, a, b, eps=1e-5, max_iter=1000):
    """
    Реализация метода половинного деления для решения уравнения f(x) = 0.
    """
    # Проверка значений на концах интервала
    fa, fb = f(a), f(b)
    if fa is None or fb is None:
        raise ValueError("Функция вернула None на конце интервала")
    if math.isnan(fa) or math.isnan(fb):
        raise ValueError("Функция вернула NaN на конце интервала")
    
    if fa * fb > 0:
        raise ValueError("Функция должна иметь разные знаки на концах интервала")
    
    n = 0
    while (b - a) > eps and n < max_iter:
        x = (a + b) / 2
        fx = f(x)
        if fx is None or math.isnan(fx):
            raise ValueError(f"Функция вернула недопустимое значение при x={x}")
        
        n += 1
        
        if abs(fx) < 1e-15:  # Учитываем машинную точность
            return x, fx, n
            
        if fa * fx < 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    
    x = (a + b) / 2
    return x, f(x), n

def input_float(prompt):
    """Ввод числа с обработкой ошибок"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка! Пожалуйста, введите число.")

# Основная программа
if __name__ == "__main__":
    print("Решение нелинейных уравнений методом половинного деления")
    print("Доступные функции: sin, cos, tan, asin, acos, atan, sqrt, exp, log, log10, pi, e")
    print("Примеры уравнений: 5*sin(x) - x + 1, atan(x-1) + 2*x")
    
    # Ввод уравнения
    equation = input("Введите уравнение (используйте 'x' как переменную): ")
    try:
        f = safe_eval(equation)
        # Тестовый вызов для проверки функции
        test_val = f(0.0)
        if test_val is None or math.isnan(test_val):
            raise ValueError("Функция возвращает недопустимое значение при x=0.0")
    except Exception as e:
        print(f"Ошибка в уравнении: {e}")
        exit()
    
    # Ввод интервала
    print("\nВведите интервал [a, b] для поиска корня:")
    a = input_float("a = ")
    b = input_float("b = ")
    
    # Ввод точности
    eps = input_float("Введите точность (например, 0.0001): ")
    
    try:
        # Решение уравнения
        x, f_x, n = bisection(f, a, b, eps)
        
        # Вывод результатов
        print("\nРезультаты:")
        print(f"Найденный корень: x = {x:.8f}")
        print(f"Значение функции: f(x) = {f_x:.2e}")
        print(f"Количество итераций: {n}")
        
        # Визуализация
        x_vals = np.linspace(a, b, 400)
        y_vals = [f(x_val) for x_val in x_vals]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', label=f'$f(x) = {equation}$')
        plt.axhline(0, color='k', linewidth=0.5)
        plt.scatter([x], [0], c='red', label=f'Корень: {x:.6f}')
        plt.title('График функции и найденный корень')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid()
        plt.show()
        
    except Exception as e:
        print(f"\nОшибка при выполнении: {e}")
        print("Убедитесь, что:")
        print("1. Уравнение записано правильно (например, используйте 0.5 вместо 0,5)")
        print("2. Функция имеет разные знаки на концах интервала")
        print("3. Функция определена на всем интервале [a, b]")
        print("4. Используйте только разрешенные функции и константы")