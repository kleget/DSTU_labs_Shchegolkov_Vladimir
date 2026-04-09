import numpy as np
import matplotlib.pyplot as plt

X = np.array([6.9, 6.4, 5.5, 7.6, 7.2, 6.8, 7.9, 5.2, 5.5, 7.5, 6.1, 5.8])
Y = np.array([-6.3, 13.1, 11.6, 0.4, -6.9, -6.1, 16.0, 0.9, 5.7, 15.2, 13.1, -5.7])

n = len(X)
alpha = 0.05

t_crit = 2.228      # для df = 10, a = 0.05
F_crit = 2.94       # для df1 = 1, df2 = 10, a = 0.05

sum_x = np.sum(X)
sum_y = np.sum(Y)
sum_x2 = np.sum(X**2)
sum_y2 = np.sum(Y**2)
sum_xy = np.sum(X * Y)

x_mean = sum_x / n
y_mean = sum_y / n

SS_xx = sum_x2 - n * x_mean**2
SS_yy = sum_y2 - n * y_mean**2
SS_xy = sum_xy - n * x_mean * y_mean

b1 = SS_xy / SS_xx
b0 = y_mean - b1 * x_mean

print(f"Уравнение регрессии: y = {b0:.4f} + {b1:.4f} * x")
print(f"Средние значения: x̅ = {x_mean:.4f}, y̅ = {y_mean:.4f}")

r = SS_xy / np.sqrt(SS_xx * SS_yy)
print(f"\nКоэффициент корреляции: r = {r:.4f}")
if abs(r) < 0.3:
    print("Оценка связи: очень слабая")
elif abs(r) < 0.5:
    print("Оценка связи: слабая")
elif abs(r) < 0.7:
    print("Оценка связи: умеренная")
elif abs(r) < 0.9:
    print("Оценка связи: сильная")
else:
    print("Оценка связи: очень сильная")

t_r = r * np.sqrt(n - 2) / np.sqrt(1 - r**2)

y_pred = b0 + b1 * X
residuals = Y - y_pred
SS_res = np.sum(residuals**2)
print(f"\nОстаточная сумма квадратов (SS_res): {SS_res:.4f}")

S2_res = SS_res / (n - 2)
S_res = np.sqrt(S2_res)
print(f"Остаточная дисперсия: S²_res = {S2_res:.4f}")
print(f"Стандартная ошибка регрессии: S_res = {S_res:.4f}")

SE_b1 = S_res / np.sqrt(SS_xx)
SE_b0 = S_res * np.sqrt(1/n + x_mean**2 / SS_xx)

t_b1 = b1 / SE_b1
t_b0 = b0 / SE_b0

print(f"\nПРОВЕРКА ЗНАЧИМОСТИ КОЭФФИЦИЕНТОВ РЕГРЕССИИ")
print(f"Коэффициент b1: значение = {b1:.4f}, стандартная ошибка = {SE_b1:.4f}, t_набл = {t_b1:.4f}")
print(f"Коэффициент b0: значение = {b0:.4f}, стандартная ошибка = {SE_b0:.4f}, t_набл = {t_b0:.4f}")
print(f"Критическое значение t (α=0.05, df={n-2}): t_кр = {t_crit:.4f}")

if abs(t_b1) > t_crit:
    print("b1: коэффициент ЗНАЧИМ")
else:
    print("b1: коэффициент НЕ ЗНАЧИМ")

if abs(t_b0) > t_crit:
    print("b0: коэффициент ЗНАЧИМ")
else:
    print("b0: коэффициент НЕ ЗНАЧИМ")

beta1_ci_lower = b1 - t_crit * SE_b1
beta1_ci_upper = b1 + t_crit * SE_b1
print(f"\nДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ ДЛЯ β1 (α=0.05):")
print(f"[{beta1_ci_lower:.4f}; {beta1_ci_upper:.4f}]")
if beta1_ci_lower < 0 < beta1_ci_upper:
    print("Интервал содержит 0, следовательно β1 не значим")

corrected_var_y = SS_yy / (n - 1)
MS_res = SS_res / (n - 2)
F_obs = corrected_var_y / MS_res

print(f"\nЗначимость уравнения регрессии (F-критерий)")
print(f"F_набл = {F_obs:.4f}")
print(f"F_кр = {F_crit:.4f}")
if F_obs > F_crit:
    print("Вывод: уравнение регрессии ЗНАЧИМО")
else:
    print("Вывод: уравнение регрессии НЕ ЗНАЧИМО")

x_grid = np.linspace(min(X) - 0.5, max(X) + 0.5, 100)
y_grid = b0 + b1 * x_grid

se_mean = S_res * np.sqrt(1/n + (x_grid - x_mean)**2 / SS_xx)

ci_upper = y_grid + t_crit * se_mean
ci_lower = y_grid - t_crit * se_mean

print(f"\nДоверительные границы для уравнения регрессии (для x̅ = {x_mean:.2f}):")
print(f"ŷ(x̅) = {b0 + b1 * x_mean:.4f}")
print(f"Доверительный интервал: [{ci_lower[50]:.4f}; {ci_upper[50]:.4f}]")

plt.figure(figsize=(12, 8))

plt.scatter(X, Y, color='blue', s=50, label='Исходные данные', zorder=5)
plt.plot(x_grid, y_grid, color='red', linewidth=2, label=f'Линия регрессии: y = {b0:.3f} + {b1:.3f}x', zorder=4)
plt.fill_between(x_grid, ci_lower, ci_upper, color='red', alpha=0.15, label=f'Доверительная область (α=0.05) для среднего Y', zorder=1)
plt.plot(x_grid, ci_lower, 'r--', linewidth=1, alpha=0.7)
plt.plot(x_grid, ci_upper, 'r--', linewidth=1, alpha=0.7)

plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)
plt.title('Линейная регрессия с доверительными границами', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

plt.figtext(0.02, 0.02,
            f"Уравнение: y = {b0:.3f} + {b1:.3f}x\n"
            f"r = {r:.4f}\n"
            f"F_набл = {F_obs:.4f}",
            bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()