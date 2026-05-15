import numpy as np
import pandas as pd
from scipy.stats import norm, chi2

# Данные варианта
vals = np.array([
    4.9, 8.4, 14.5, 8.6, 16.0, 14.1, 10.7, 6.3, 12.6, 1.1,
    11.7, 14.7, 4.7, 15.2, 23.7, 0.3, 10.4, 5.6, 13.1, 8.0,
    11.5, -0.7, 9.9, 11.9, 13.4, 9.7, 11.4, 13.5, 0.1, 9.1,
    8.7, 18.6, 7.2, -5.4, 3.3, 8.3, 7.8, 9.7, 10.0, 7.3,
    10.8, 6.9, 13.4, 10.1, 0.1, 11.4, -2.7, 9.0, 14.4, 12.1
])

alpha = 0.05
n = len(vals)

# Интервалы из расчета
bounds = np.array([-5.4, -1.2, 3.0, 7.2, 11.4, 15.6, 19.8, 24.0])

def count_intervals(x, bounds):
    counts = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if i == 0:
            c = np.sum((x >= a) & (x <= b))
        else:
            c = np.sum((x > a) & (x <= b))
        counts.append(c)
    return np.array(counts)

counts = count_intervals(vals, bounds)

x_mean = np.mean(vals)
s_std = np.std(vals, ddof=1)

print("n =", n)
print("x_mean =", round(x_mean, 3))
print("s_std =", round(s_std, 3))
print("частоты по интервалам:", counts.tolist())

# -----------------------------
# 1) Пирсон: нормальное распределение
# -----------------------------
# Малые частоты на краях объединяем:
# [-5.4; -1.2] + (-1.2; 3.0] -> (-inf; 3.0]
# (15.6; 19.8] + (19.8; 24.0] -> (15.6; +inf)
obs_norm = np.array([
    counts[0] + counts[1],
    counts[2],
    counts[3],
    counts[4],
    counts[5] + counts[6]
])

norm_bounds = [(-np.inf, 3.0), (3.0, 7.2), (7.2, 11.4), (11.4, 15.6), (15.6, np.inf)]

p_norm = []
for a, b in norm_bounds:
    left = 0 if a == -np.inf else norm.cdf(a, loc=x_mean, scale=s_std)
    right = 1 if b == np.inf else norm.cdf(b, loc=x_mean, scale=s_std)
    p_norm.append(right - left)

p_norm = np.array(p_norm)
exp_norm = n * p_norm
chi_norm = np.sum((obs_norm - exp_norm) ** 2 / exp_norm)

r_norm = len(obs_norm) - 1 - 2
crit_norm = chi2.ppf(1 - alpha, r_norm)

table_norm = pd.DataFrame({
    "интервал": ["(-∞; 3.0]", "(3.0; 7.2]", "(7.2; 11.4]", "(11.4; 15.6]", "(15.6; +∞)"],
    "n_i": obs_norm,
    "P_i": np.round(p_norm, 4),
    "nP_i": np.round(exp_norm, 2),
    "вклад": np.round((obs_norm - exp_norm) ** 2 / exp_norm, 3)
})

print("\nПирсон: нормальное распределение")
print(table_norm.to_string(index=False))
print("chi_emp =", round(chi_norm, 3))
print("r =", r_norm)
print("chi_crit =", round(crit_norm, 3))
print("Вывод:", "H0 не отвергается" if chi_norm < crit_norm else "H0 отвергается")

# -----------------------------
# 2) Пирсон: равномерное распределение
# -----------------------------
# Для равномерного распределения на [a; b] все интервалы одинаковой длины,
# поэтому вероятность каждого интервала равна 1/k.
a_uni = bounds[0]
b_uni = bounds[-1]
k_uni = len(counts)

p_uni = np.ones(k_uni) / k_uni
exp_uni = n * p_uni
chi_uni = np.sum((counts - exp_uni) ** 2 / exp_uni)

# a и b взяты по выборке, поэтому считаем, что оценивали 2 параметра
r_uni = k_uni - 1 - 2
crit_uni = chi2.ppf(1 - alpha, r_uni)

table_uni = pd.DataFrame({
    "интервал": [f"({bounds[i]}; {bounds[i+1]}]" if i > 0 else f"[{bounds[i]}; {bounds[i+1]}]" for i in range(k_uni)],
    "n_i": counts,
    "P_i": np.round(p_uni, 4),
    "nP_i": np.round(exp_uni, 2),
    "вклад": np.round((counts - exp_uni) ** 2 / exp_uni, 3)
})

print("\nПирсон: равномерное распределение")
print(table_uni.to_string(index=False))
print("chi_emp =", round(chi_uni, 3))
print("r =", r_uni)
print("chi_crit =", round(crit_uni, 3))
print("Вывод:", "H0 не отвергается" if chi_uni < crit_uni else "H0 отвергается")
