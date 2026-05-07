import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Данные
x_values = np.array([
    4.9, 8.4, 14.5, 8.6, 16.0, 14.1, 10.7, 6.3, 12.6, 1.1,
    11.7, 14.7, 4.7, 15.2, 23.7, 0.3, 10.4, 5.6, 13.1, 8.0,
    11.5, -0.7, 9.9, 11.9, 13.4, 9.7, 11.4, 13.5, 0.1, 9.1,
    8.7, 18.6, 7.2, -5.4, 3.3, 8.3, 7.8, 9.7, 10.0, 7.3,
    10.8, 6.9, 13.4, 10.1, 0.1, 11.4, -2.7, 9.0, 14.4, 12.1
])

n = len(x_values)

# Считаем среднее и дисперсию
x_mean = np.mean(x_values)
s_std = np.std(x_values, ddof=1)

print(f"n = {n}, x̄ = {x_mean:.3f}, S = {s_std:.3f}")

# Гистограмма
plt.hist(x_values, bins=7, edgecolor='black', alpha=0.7)
plt.title("Гистограмма значений")
plt.xlabel("x")
plt.ylabel("Частота")
plt.grid(True)
plt.show()