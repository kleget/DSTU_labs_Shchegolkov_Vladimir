import numpy as np
from sympy import symbols, sympify, lambdify
import matplotlib.pyplot as plt


def validate_input(func_str, a_str, b_str, eps_str):
    """
    Проверяет корректность введенных пользователем данных
    Возвращает список ошибок, если они есть
    """
    errors = []
    
    # Проверка функции: должна быть непустой и математически корректной
    if not func_str.strip():
        errors.append("Функция не введена")
    else:
        try:
            x = symbols("x")
            sympify(func_str)  # Пробуем преобразовать строку в математическое выражение
        except Exception as e:
            errors.append(f"Ошибка в функции: {str(e)}")
    
    # Проверка границ интервала: должны быть числами и a < b
    try:
        a_val = float(a_str)
    except ValueError:
        errors.append("Левая граница 'a' должна быть числом")
        
    try:
        b_val = float(b_str)
    except ValueError:
        errors.append("Правая граница 'b' должна быть числом")
        
    if len(errors) == 0 and a_val >= b_val:
        errors.append("Левая граница 'a' должна быть меньше правой границы 'b'")
        
    # Проверка точности: должно быть положительное число
    try:
        eps = float(eps_str)
        if eps <= 0:
            errors.append("Точность 'ε' должна быть положительным числом")
    except ValueError:
        errors.append("Точность 'ε' должна быть числом")
        
    return errors


def draw_function_plot(func_str, root, a, b):
    """
    Строит график функции и отмечает найденный корень
    """
    try:
        x = symbols("x")
        f_expr = sympify(func_str)
        f = lambdify(x, f_expr, modules=["numpy"])  # Создаем функцию из строки

        # Генерируем точки для графика с запасом по краям
        x_min = min(a, b, root) - 0.5
        x_max = max(a, b, root) + 0.5
        x_vals = np.linspace(x_min, x_max, 1000)

        # Вычисляем значения функции, игнорируя математические ошибки
        with np.errstate(all="ignore"):
            y_vals = f(x_vals)
            # Отфильтровываем некорректные значения (бесконечности, NaN)
            valid_mask = np.isfinite(y_vals)
            x_vals = x_vals[valid_mask]
            y_vals = y_vals[valid_mask]

        # Создаем и настраиваем график
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, color="#4a90e2", label=f"f(x) = {func_str}")
        plt.axhline(0, color="gray", linewidth=0.8)  # Ось X
        plt.axvline(0, color="gray", linewidth=0.8)  # Ось Y
        plt.scatter([root], [0], color="red", s=50, label=f"Корень: {root:.6f}")  # Корень
        plt.scatter([a, b], [f(a), f(b)], color="green", s=30, label="Границы")  # Границы

        # Оформление графика
        plt.grid(True, color="#cccccc", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.gca().set_facecolor("#ffffff")
        plt.title("График функции и найденный корень")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Не удалось построить график функции: {str(e)}")
        print("Возможно, функция не определена на всем интервале или имеет особенности.")


def bisection_method():
    """
    Основная функция - реализация метода половинного деления
    """
    print("=" * 60)
    print("МЕТОД ПОЛОВИННОГО ДЕЛЕНИЯ")
    print("=" * 60)
    
    # Ввод данных от пользователя
    func_str = input("Введите функцию f(x) (например, tan(x)**3 - x + 1): ").strip()
    a_str = input("Введите левую границу a (например, -1.0): ").strip()
    b_str = input("Введите правую границу b (например, 0.5): ").strip()
    eps_str = input("Введите точность ε (по умолчанию 0.001): ").strip()
    
    # Установка точности по умолчанию
    if not eps_str:
        eps_str = "0.001"
    
    # Проверка корректности введенных данных
    errors = validate_input(func_str, a_str, b_str, eps_str)
    if errors:
        print("\nОшибки во входных данных:")
        for error in errors:
            print(f"• {error}")
        return
    
    try:
        # Преобразование введенных данных в числа
        a_val = float(a_str)
        b_val = float(b_str)
        eps = float(eps_str)
        
        # Создание математической функции из строки
        x = symbols("x")
        f_expr = sympify(func_str)
        f = lambdify(x, f_expr, modules=["numpy"])
        
        # Проверка условия сходимости метода
        fa = f(a_val)
        fb = f(b_val)
        
        # Условие сходимости: f(a) * f(b) < 0 (функция меняет знак)
        if fa * fb > 0:
            print("\n❌ Условия сходимости не выполнены!")
            print(f"Для метода половинного деления требуется, чтобы функция имела разные знаки на концах интервала.")
            print(f"Текущие значения:")
            print(f"f({a_val:.3f}) = {fa:.3f}")
            print(f"f({b_val:.3f}) = {fb:.3f}")
            print("Пожалуйста, выберите другой интервал [a, b], где функция меняет знак.")
            return
        
        # Инициализация переменных для метода
        a = a_val
        b = b_val
        iteration = 0
        max_iterations = 1000  # Защита от бесконечного цикла
        
        # Заголовок таблицы итераций
        print("\n" + "=" * 80)
        print(f"{'n':<3} {'a':<15} {'b':<15} {'c':<15} {'f(c)':<15}")
        print("-" * 80)
        
        # ОСНОВНОЙ ЦИКЛ МЕТОДА ПОЛОВИННОГО ДЕЛЕНИЯ
        while iteration < max_iterations:
            iteration += 1
            c = (a + b) / 2      # Середина текущего интервала
            fc = f(c)            # Значение функции в середине
            
            # Вывод информации о текущей итерации
            print(f"{iteration:<3} {a:<15.8f} {b:<15.8f} {c:<15.8f} {fc:<15.8e}")
            
            # Критерии остановки:
            # 1. Найден точный корень (значение функции очень близко к 0)
            if abs(fc) < 1e-12:
                break
                
            # 2. Достигнута требуемая точность
            if abs(fc) <= eps and abs(b - a) <= eps:
                break
            
            # Выбор нового интервала: выбираем ту половину, где функция меняет знак
            if f(a) * fc > 0:
                a = c  # Корень в правой половине
            else:
                b = c  # Корень в левой половине
        
        # Вывод окончательных результатов
        root = (a + b) / 2
        print("-" * 80)
        
        # Предупреждение о достижении максимального числа итераций
        if iteration == max_iterations:
            print("Предупреждение: Достигнуто максимальное число итераций. Решение может быть неточным.")
        
        # Итоговый результат
        print(f"\nРЕЗУЛЬТАТ:")
        print(f"Корень: {root:.8f}")
        print(f"Значение функции: {f(root):.3e}")
        print(f"Количество итераций: {iteration}")
        
        # Предложение построить график
        plot_choice = input("\nПостроить график? (y/n): ").strip().lower()
        if plot_choice in ['y', 'yes', 'д', 'да']:
            draw_function_plot(func_str, root, a_val, b_val)
            
    except Exception as e:
        # Обработка ошибок при вычислениях
        print(f"\nОшибка при выполнении вычислений: {str(e)}")
        print("Проверьте корректность введенной функции и параметров.")


if __name__ == "__main__":
    # Запуск программы
    bisection_method()