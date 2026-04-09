import numpy as np

raw_data = [
    4.9, 8.4, 14.5, 8.6, 16.0, 14.1, 10.7, 6.3, 12.6, 1.1,
    11.7, 14.7, 4.7, 15.2, 23.7, 0.3, 10.4, 5.6, 13.1, 8.0,
    11.5, -0.7, 9.9, 11.9, 13.4, 9.7, 11.4, 13.5, 0.1, 9.1,
    8.7, 18.6, 7.2, -5.4, 3.3, 8.3, 7.8, 9.7, 10.0, 7.3,
    10.8, 6.9, 13.4, 10.1, 0.1, 11.4, -2.7, 9.0, 14.4, 12.1
]

n = len(raw_data)
k = int(1 + np.log2(n))
print(f"Объем выборки: n = {n}")
print(f"Рекомендуемое количество интервалов: k = {k}")

min_val = min(raw_data)
max_val = max(raw_data)
r = max_val - min_val
h = r / k

print(f"x_min = {min_val}")
print(f"x_max = {max_val}")
print(f"Размах R = {r}")
print(f"Длина интервала h = {h:.4f}")

bins = np.linspace(min_val, max_val, k + 1)
hist, bin_edges = np.histogram(raw_data, bins=bins)

interval_data = []
for i in range(len(hist)):
    left = round(bin_edges[i], 2)
    right = round(bin_edges[i + 1], 2)
    freq = int(hist[i])
    interval_data.append((left, right, freq))

print("\nИнтервальный ряд:")
for left, right, freq in interval_data:
    print(f"({left:.2f}, {right:.2f}, {freq})")
