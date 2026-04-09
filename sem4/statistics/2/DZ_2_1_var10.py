import sys

import numpy as np

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

X = np.array([6.7, 5.4, 7.7, 6.6, 7.7, 5.5, 6.0, 7.3, 7.9, 6.3, 6.1, 5.5], dtype=float)
Y = np.array([7.2, 11.3, 7.9, 0.7, 16.9, -5.4, -5.5, 1.0, -7.0, 12.9, 12.8, 0.6], dtype=float)

n = len(X)
alpha = 0.05
t_crit = 2.228
F_crit = 4.96

x_mean = np.mean(X)
y_mean = np.mean(Y)

SS_xx = np.sum((X - x_mean) ** 2)
SS_yy = np.sum((Y - y_mean) ** 2)
SS_xy = np.sum((X - x_mean) * (Y - y_mean))

b1 = SS_xy / SS_xx
b0 = y_mean - b1 * x_mean

y_pred = b0 + b1 * X
residuals = Y - y_pred

SSE = np.sum(residuals ** 2)
MSE = SSE / (n - 2)
S = np.sqrt(MSE)

SE_b1 = S / np.sqrt(SS_xx)
SE_b0 = S * np.sqrt(1 / n + x_mean ** 2 / SS_xx)

t_b1 = b1 / SE_b1
t_b0 = b0 / SE_b0

SSR = np.sum((y_pred - y_mean) ** 2)
R2 = SSR / SS_yy
r = SS_xy / np.sqrt(SS_xx * SS_yy)
F_obs = (SSR / 1) / MSE

beta1_ci = (b1 - t_crit * SE_b1, b1 + t_crit * SE_b1)

x_grid = np.linspace(np.min(X) - 0.3, np.max(X) + 0.3, 200)
y_grid = b0 + b1 * x_grid
band = t_crit * S * np.sqrt(1 / n + (x_grid - x_mean) ** 2 / SS_xx)
ci_lower = y_grid - band
ci_upper = y_grid + band

y_center = b0 + b1 * x_mean
center_band = t_crit * S * np.sqrt(1 / n)

print("ЗАДАНИЕ 1. ЛИНЕЙНАЯ РЕГРЕССИЯ")
print(f"n = {n}, alpha = {alpha}")
print()
print("Исходные статистики:")
print(f"x̄ = {x_mean:.4f}")
print(f"ȳ = {y_mean:.4f}")
print(f"S_xx = {SS_xx:.4f}")
print(f"S_yy = {SS_yy:.4f}")
print(f"S_xy = {SS_xy:.4f}")
print()
print("Уравнение регрессии:")
print(f"ŷ = {b0:.4f} + {b1:.4f}x")
print()
print("Проверка значимости коэффициентов:")
print(f"SE(b0) = {SE_b0:.4f}")
print(f"SE(b1) = {SE_b1:.4f}")
print(f"t(b0) = {t_b0:.4f}")
print(f"t(b1) = {t_b1:.4f}")
print(f"t_crit = {t_crit:.3f}")
print(f"b0 значим: {'да' if abs(t_b0) > t_crit else 'нет'}")
print(f"b1 значим: {'да' if abs(t_b1) > t_crit else 'нет'}")
print()
print("Доверительный интервал для beta1:")
print(f"[{beta1_ci[0]:.4f}; {beta1_ci[1]:.4f}]")
print()
print("Проверка значимости уравнения регрессии:")
print(f"SSE = {SSE:.4f}")
print(f"SSR = {SSR:.4f}")
print(f"MSE = {MSE:.4f}")
print(f"F_obs = {F_obs:.4f}")
print(f"F_crit = {F_crit:.2f}")
print(f"Уравнение значимо: {'да' if F_obs > F_crit else 'нет'}")
print()
print("Дополнительно:")
print(f"r = {r:.4f}")
print(f"R^2 = {R2:.4f}")
print(
    "Доверительные границы для среднего отклика при x = x̄: "
    f"[{y_center - center_band:.4f}; {y_center + center_band:.4f}]"
)

if plt is None:
    print()
    print("matplotlib не установлен, поэтому график не построен.")
else:
    plt.figure(figsize=(11, 7))
    plt.scatter(X, Y, s=60, color="royalblue", label="Исходные данные", zorder=3)
    plt.plot(x_grid, y_grid, color="crimson", linewidth=2, label=f"ŷ = {b0:.3f} + {b1:.3f}x")
    plt.fill_between(
        x_grid,
        ci_lower,
        ci_upper,
        color="salmon",
        alpha=0.25,
        label="95% доверительные границы для E(Y|X=x)",
    )
    plt.plot(x_grid, ci_lower, "--", color="crimson", linewidth=1)
    plt.plot(x_grid, ci_upper, "--", color="crimson", linewidth=1)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Вариант 10. Задание 1. Линейная регрессия")
    plt.grid(alpha=0.3)
    plt.legend(loc="best")
    plt.figtext(
        0.02,
        0.02,
        f"t(b1) = {t_b1:.4f}, F = {F_obs:.4f}, R² = {R2:.4f}",
        bbox={"facecolor": "white", "alpha": 0.85},
    )
    plt.tight_layout()
    plt.show()
