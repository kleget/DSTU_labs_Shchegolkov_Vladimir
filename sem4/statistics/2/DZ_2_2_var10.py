
import numpy as np


X = np.array([6.7, 5.4, 7.7, 6.6, 7.7, 5.5, 6.0, 7.3, 7.9, 6.3, 6.1, 5.5], dtype=float)
Y = np.array([7.2, 11.3, 7.9, 0.7, 16.9, -5.4, -5.5, 1.0, -7.0, 12.9, 12.8, 0.6], dtype=float)

n = len(X)
p = 4
alpha = 0.05
t_crit = 2.306
F_crit = 4.07

X_design = np.column_stack((np.ones(n), X, X ** 2, X ** 3))
XtX = X_design.T @ X_design
XtX_inv = np.linalg.inv(XtX)
coef = XtX_inv @ X_design.T @ Y

Y_pred = X_design @ coef
residuals = Y - Y_pred

RSS = np.sum(residuals ** 2)
MSE = RSS / (n - p)
cov_matrix = MSE * XtX_inv
se = np.sqrt(np.diag(cov_matrix))
t_stats = coef / se

y_mean = np.mean(Y)
TSS = np.sum((Y - y_mean) ** 2)
SSR = np.sum((Y_pred - y_mean) ** 2)
R2 = SSR / TSS
F_obs = (SSR / (p - 1)) / MSE

print("ЗАДАНИЕ 2. НЕЛИНЕЙНАЯ РЕГРЕССИЯ ТРЕТЬЕЙ СТЕПЕНИ")
print(f"n = {n}, p = {p}, alpha = {alpha}")
print()
print("Уравнение регрессии:")
print(
    f"ŷ = { [0]:.6f} "
    f"+ {coef[1]:.6f}x "
    f"+ {coef[2]:.6f}x² "
    f"+ {coef[3]:.6f}x³"
)
print()
print("Проверка значимости коэффициентов:")
print(f"t_crit = {t_crit:.3f} при df = {n - p}")
for name, value, err, t_value in zip(("b0", "b1", "b2", "b3"), coef, se, t_stats):
    is_significant = abs(t_value) > t_crit
    print(
        f"{name}: coef = {value:.6f}, SE = {err:.6f}, "
        f"t = {t_value:.4f}, значим: {'да' if is_significant else 'нет'}"
    )

print()
print("Проверка значимости уравнения в целом:")
print(f"RSS = {RSS:.4f}")
print(f"SSR = {SSR:.4f}")
print(f"MSE = {MSE:.4f}")
print(f"R^2 = {R2:.4f}")
print(f"F_obs = {F_obs:.4f}")
print(f"F_crit = {F_crit:.2f} при df1 = 3, df2 = 8")
print(f"Уравнение значимо: {'да' if F_obs > F_crit else 'нет'}")
