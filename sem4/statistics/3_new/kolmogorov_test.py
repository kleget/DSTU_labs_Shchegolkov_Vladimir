import numpy as np
from scipy.stats import norm

# Сортировка данных
x_values = np.array([
    4.9, 8.4, 14.5, 8.6, 16.0, 14.1, 10.7, 6.3, 12.6, 1.1,
    11.7, 14.7, 4.7, 15.2, 23.7, 0.3, 10.4, 5.6, 13.1, 8.0,
    11.5, -0.7, 9.9, 11.9, 13.4, 9.7, 11.4, 13.5, 0.1, 9.1,
    8.7, 18.6, 7.2, -5.4, 3.3, 8.3, 7.8, 9.7, 10.0, 7.3,
    10.8, 6.9, 13.4, 10.1, 0.1, 11.4, -2.7, 9.0, 14.4, 12.1
])

n = len(x_values)
x_mean = np.mean(x_values)
s_std = np.std(x_values, ddof=1)

# эмпирическая функция распределения
x_sorted = np.sort(x_values)
F_n = np.arange(1, n+1) / n

# теоретическая функция распределения (нормальная)
F_0 = norm.cdf(x_sorted, loc=x_mean, scale=s_std)

# D_n
D_n = np.max(np.abs(F_n - F_0))

# λ эмпирическое
lambda_emp = D_n * np.sqrt(n)

# критическое значение λ
lambda_crit = 1.36  # при α=0.05

print("Критерий Колмогорова")
print(f"D_n = {D_n:.4f}, λ = {lambda_emp:.3f}")
print(f"λ критическое = {lambda_crit}")
print("H₀ не отвергается" if lambda_emp < lambda_crit else "H₀ отвергается")