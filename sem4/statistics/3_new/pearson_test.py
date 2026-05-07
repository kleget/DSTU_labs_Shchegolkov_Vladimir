import numpy as np
from scipy.stats import norm, chi2

# Данные и интервалы (после объединения маленьких частот)
intervals = [(-5.4, 3.0), (3.0, 7.2), (7.2, 11.4), (11.4, 15.6), (15.6, 24)]
observed = np.array([7, 7, 19, 14, 3])

n = np.sum(observed)

# Параметры нормального распределения
x_mean = 8.852
s_std = 5.061

# Теоретические вероятности для каждого интервала
P = [norm.cdf(b, x_mean, s_std) - norm.cdf(a, x_mean, s_std) for (a, b) in intervals]

# Теоретические частоты
n_expected = n * np.array(P)

# χ²
chi_sq = np.sum((observed - n_expected)**2 / n_expected)

# Степени свободы: k - 1 - 2 (оценивали x̄ и S)
r = len(observed) - 1 - 2

# Критическое значение
chi_crit = chi2.ppf(0.95, r)

print("Критерий Пирсона")
print(f"χ² эмпирическое = {chi_sq:.3f}")
print(f"χ² критическое = {chi_crit:.3f}")
print("H₀ не отвергается" if chi_sq < chi_crit else "H₀ отвергается")