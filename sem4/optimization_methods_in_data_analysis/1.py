import numpy as np
import matplotlib.pyplot as plt

# ==============================
# ДАННЫЕ
# ==============================

# Таблица 1 (интерполяция)
x1 = np.array([0.11, 0.15, 0.21, 0.29, 0.35, 0.40], dtype=float)
y1 = np.array([9.05421, 6.61659, 4.69170, 3.351069, 2.73951, 2.36522], dtype=float)
x_star = 0.3535

# Таблица 2 (МНК)
x2 = np.array([5.59, 5.66, 5.30, 5.57, 5.48, 5.37, 5.41, 5.61], dtype=float)
y2 = np.array([113.8, 119.56, 105.32, 119.6, 100.5, 114.8, 115.53, 117.9], dtype=float)

# ==============================
# ФУНКЦИИ
# ==============================

# Интерполяция Лагранжа
def lagrange_interpolation(x, y, x_val):
    n = len(x)
    result = 0.0

    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (x_val - x[j]) / (x[i] - x[j])
        result += term

    return result


# Интерполяция Ньютона (разделенные разности)
def newton_interpolation(x, y, x_val):
    n = len(x)
    coef = np.copy(y)

    # таблица разделенных разностей
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j-1:n-1]) / (x[j:n] - x[0:n-j])

    # вычисление значения многочлена
    result = coef[n-1]
    for k in range(n-2, -1, -1):
        result = result * (x_val - x[k]) + coef[k]

    return result


# Метод наименьших квадратов (своими руками)
def least_squares_poly(x, y, degree):
    # строим матрицу Вандермонда
    X = np.vander(x, degree + 1, increasing=True)

    # нормальные уравнения: (X^T X)a = X^T y
    A = X.T @ X
    B = X.T @ y

    coeffs = np.linalg.solve(A, B)
    return coeffs


# вычисление значений полинома
def poly_value(coeffs, x):
    y_val = 0
    for i, a in enumerate(coeffs):
        y_val += a * x**i
    return y_val


# коэффициент корреляции (Пирсон)
def correlation_index(y_true, y_pred):
    y_mean = np.mean(y_true)

    num = np.sum((y_true - y_mean) * (y_pred - np.mean(y_pred)))
    den = np.sqrt(np.sum((y_true - y_mean)**2) * np.sum((y_pred - np.mean(y_pred))**2))

    return num / den


# ==============================
# ЗАДАНИЕ 1: ИНТЕРПОЛЯЦИЯ
# ==============================

y_lagrange = lagrange_interpolation(x1, y1, x_star)
y_newton = newton_interpolation(x1, y1, x_star)

print("===== ЗАДАНИЕ 1 =====")
print(f"x* = {x_star}")
print(f"Интерполяция Лагранжа: y = {y_lagrange:.6f}")
print(f"Интерполяция Ньютона : y = {y_newton:.6f}")

# график интерполяции
x_plot = np.linspace(min(x1), max(x1), 400)
y_plot_lagrange = np.array([lagrange_interpolation(x1, y1, xx) for xx in x_plot])

plt.figure()
plt.plot(x_plot, y_plot_lagrange, label="Lagrange polynomial")
plt.scatter(x1, y1, color="red", label="Table points")
plt.scatter([x_star], [y_lagrange], color="green", label="Interpolated value")
plt.title("Interpolation (Task 1)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.legend()
plt.show()


# ==============================
# ЗАДАНИЕ 2: МНК (1,2,3 степень)
# ==============================

print("\n===== ЗАДАНИЕ 2 (МНК) =====")

degrees = [1, 2, 3]

for deg in degrees:
    coeffs = least_squares_poly(x2, y2, deg)
    y_pred = poly_value(coeffs, x2)
    r = correlation_index(y2, y_pred)

    print(f"\n--- Полином степени {deg} (МНК вручную) ---")
    print("Коэффициенты:", coeffs)
    print("Корреляция r =", round(r, 6))

# ==============================
# СРАВНЕНИЕ С БИБЛИОТЕКАМИ (numpy.polyfit)
# ==============================

print("\n===== СРАВНЕНИЕ С numpy.polyfit =====")

for deg in degrees:
    # polyfit возвращает в обратном порядке (старшая степень -> младшая)
    p = np.polyfit(x2, y2, deg)
    y_pred_lib = np.polyval(p, x2)

    # переведем в вид a0+a1x+...
    coeffs_lib = p[::-1]

    r_lib = correlation_index(y2, y_pred_lib)

    print(f"\n--- Полином степени {deg} (numpy.polyfit) ---")
    print("Коэффициенты:", coeffs_lib)
    print("Корреляция r =", round(r_lib, 6))

# ==============================
# ГРАФИКИ ДЛЯ МНК
# ==============================

x_dense = np.linspace(min(x2), max(x2), 400)

plt.figure()
plt.scatter(x2, y2, color="black", label="Experimental points")

for deg in degrees:
    coeffs = least_squares_poly(x2, y2, deg)
    y_dense = poly_value(coeffs, x_dense)
    plt.plot(x_dense, y_dense, label=f"LS degree {deg}")

plt.title("Least Squares Approximation (Task 2)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.legend()
plt.show()