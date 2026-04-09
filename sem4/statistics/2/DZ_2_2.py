import numpy as np
# Данные
X = np.array([6.9, 6.4, 5.5, 7.6, 7.2, 6.8, 7.9, 5.2, 5.5, 7.5, 6.1, 5.8])
Y = np.array([-6.3, 13.1, 11.6, 0.4, -6.9, -6.1, 16.0, 0.9, 5.7, 15.2, 13.1, -5.7])

n = len(X)
p = 4
alpha = 0.05 
t_crit = 2.306 #для числа степеней свободы = 8

X_design = np.column_stack([np.ones(n), X, X**2, X**3])

#оценка коэффициентов методом наименьших квадратов
XtX = X_design.T @ X_design
XtX_inv = np.linalg.inv(XtX)
XtY = X_design.T @ Y
coef = XtX_inv @ XtY       #b0, b1, b2, b3

Y_pred = X_design @ coef
residuals = Y - Y_pred
RSS = np.sum(residuals**2)
MSE = RSS / (n - p)

cov_matrix = MSE * XtX_inv
se = np.sqrt(np.diag(cov_matrix))

t_stats = coef / se

significant = np.abs(t_stats) > t_crit

print("Нелинейная регрессия 3-й степени")
print(f"Уравнение: y = {coef[0]:.6f} + {coef[1]:.6f}·x + {coef[2]:.6f}·x² + {coef[3]:.6f}·x³\n")
print(f"Число наблюдений n = {n}")
print(f"Число параметров p = {p}")
print(f"Степени свободы: {n-p}")
print(f"Критическое значение t (α={alpha}, df={n-p}) = {t_crit}\n")
print("Коэффициенты, стандартные ошибки, t-статистики и значимость:")
print(f"{'Параметр':<8} {'Оценка':>12} {'Ст.ошибка':>12} {'t-стат':>10} {'|t| > t_кр':>12}")
for i, name in enumerate(['b0', 'b1', 'b2', 'b3']):
    sign = "да" if significant[i] else "нет"
    print(f"{name:<8} {coef[i]:>12.6f} {se[i]:>12.6f} {t_stats[i]:>10.4f} {sign:>12}")