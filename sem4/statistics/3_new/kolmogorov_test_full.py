import numpy as np
import pandas as pd
from scipy.stats import norm

# Данные варианта
vals = np.array([
    4.9, 8.4, 14.5, 8.6, 16.0, 14.1, 10.7, 6.3, 12.6, 1.1,
    11.7, 14.7, 4.7, 15.2, 23.7, 0.3, 10.4, 5.6, 13.1, 8.0,
    11.5, -0.7, 9.9, 11.9, 13.4, 9.7, 11.4, 13.5, 0.1, 9.1,
    8.7, 18.6, 7.2, -5.4, 3.3, 8.3, 7.8, 9.7, 10.0, 7.3,
    10.8, 6.9, 13.4, 10.1, 0.1, 11.4, -2.7, 9.0, 14.4, 12.1
])

n = len(vals)
alpha = 0.05

# Интервалы из расчета
bounds = np.array([-5.4, -1.2, 3.0, 7.2, 11.4, 15.6, 19.8, 24.0])
upper = bounds[1:]

counts = []
for i in range(len(bounds) - 1):
    a, b = bounds[i], bounds[i + 1]
    if i == 0:
        c = np.sum((vals >= a) & (vals <= b))
    else:
        c = np.sum((vals > a) & (vals <= b))
    counts.append(c)

counts = np.array(counts)
cum_counts = np.cumsum(counts)
F_n = cum_counts / n

x_mean = np.mean(vals)
s_std = np.std(vals, ddof=1)

# -----------------------------
# 1) Колмогоров: нормальное распределение
# -----------------------------
F_norm = norm.cdf(upper, loc=x_mean, scale=s_std)
D_norm = np.abs(F_n - F_norm)

Dmax_norm = np.max(D_norm)
lambda_norm = Dmax_norm * np.sqrt(n)

lambda_crit = 1.36
D_crit = lambda_crit / np.sqrt(n)

table_norm = pd.DataFrame({
    "x": upper,
    "F_n": np.round(F_n, 4),
    "F_0": np.round(F_norm, 4),
    "|F_n-F_0|": np.round(D_norm, 4)
})

print("Колмогоров: нормальное распределение")
print(table_norm.to_string(index=False))
print("Dmax =", round(Dmax_norm, 4))
print("lambda_emp =", round(lambda_norm, 3))
print("lambda_crit =", lambda_crit)
print("Вывод:", "H0 не отвергается" if lambda_norm < lambda_crit else "H0 отвергается")

# -----------------------------
# 2) Колмогоров: равномерное распределение
# -----------------------------
a_uni = bounds[0]
b_uni = bounds[-1]

# F0(x) для равномерного распределения на [a; b]:
# F0(x) = (x - a) / (b - a)
F_uni = (upper - a_uni) / (b_uni - a_uni)
D_uni = np.abs(F_n - F_uni)

Dmax_uni = np.max(D_uni)
lambda_uni = Dmax_uni * np.sqrt(n)

table_uni = pd.DataFrame({
    "x": upper,
    "F_n": np.round(F_n, 4),
    "F_0": np.round(F_uni, 4),
    "|F_n-F_0|": np.round(D_uni, 4)
})

print("\nКолмогоров: равномерное распределение")
print(table_uni.to_string(index=False))
print("Dmax =", round(Dmax_uni, 4))
print("lambda_emp =", round(lambda_uni, 3))
print("lambda_crit =", lambda_crit)
print("D_crit =", round(D_crit, 4))
print("Вывод:", "H0 не отвергается" if lambda_uni < lambda_crit else "H0 отвергается")
