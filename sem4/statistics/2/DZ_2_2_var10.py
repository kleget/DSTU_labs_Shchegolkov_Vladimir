import numpy as np


x_vals = np.array([6.7, 5.4, 7.7, 6.6, 7.7, 5.5, 6.0, 7.3, 7.9, 6.3, 6.1, 5.5], dtype=float)
y_vals = np.array([7.2, 11.3, 7.9, 0.7, 16.9, -5.4, -5.5, 1.0, -7.0, 12.9, 12.8, 0.6], dtype=float)

n_obs = len(x_vals)
n_coef = 4
alpha = 0.05
t_critical = 2.306
f_critical = 4.07

design_mat = np.column_stack(  # матрица признаков
    (np.ones(n_obs), x_vals, x_vals ** 2, x_vals ** 3)
)
normal_mat = design_mat.T @ design_mat
normal_inv = np.linalg.inv(normal_mat)
reg_coef = normal_inv @ design_mat.T @ y_vals 

y_pred = design_mat @ reg_coef
residuals = y_vals - y_pred

rss = np.sum(residuals ** 2)
mse = rss / (n_obs - n_coef)
coef_cov = mse * normal_inv
coef_se = np.sqrt(np.diag(coef_cov))
t_stats = reg_coef / coef_se

y_mean = np.mean(y_vals)
tss = np.sum((y_vals - y_mean) ** 2)
ssr = np.sum((y_pred - y_mean) ** 2)
r2 = ssr / tss
f_obs = (ssr / (n_coef - 1)) / mse

print("ЗАДАНИЕ 2. НЕЛИНЕЙНАЯ РЕГРЕССИЯ ТРЕТЬЕЙ СТЕПЕНИ")
print(f"n = {n_obs}, p = {n_coef}, alpha = {alpha}")
print()
print("Уравнение регрессии:")
print(
    f"ŷ = {reg_coef[0]:.6f} "
    f"+ {reg_coef[1]:.6f}x "
    f"+ {reg_coef[2]:.6f}x² "
    f"+ {reg_coef[3]:.6f}x³"
)
print()
print("Проверка значимости коэффициентов:")
print(f"t_crit = {t_critical:.3f} при df = {n_obs - n_coef}")
for coef_name, coef_value, coef_error, t_value in zip(
    ("b0", "b1", "b2", "b3"),
    reg_coef,
    coef_se,
    t_stats,
):
    is_significant = abs(t_value) > t_critical
    print(
        f"{coef_name}: coef = {coef_value:.6f}, SE = {coef_error:.6f}, "
        f"t = {t_value:.4f}, значим: {'да' if is_significant else 'нет'}"
    )

print()
print("Проверка значимости уравнения в целом:")
print(f"RSS = {rss:.4f}")
print(f"SSR = {ssr:.4f}")
print(f"MSE = {mse:.4f}")
print(f"R^2 = {r2:.4f}")
print(f"F_obs = {f_obs:.4f}")
print(f"F_crit = {f_critical:.2f} при df1 = 3, df2 = 8")
print(f"Уравнение значимо: {'да' if f_obs > f_critical else 'нет'}")
