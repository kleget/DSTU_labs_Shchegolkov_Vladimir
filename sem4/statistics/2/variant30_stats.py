import numpy as np
import matplotlib.pyplot as plt

interval_data = [
    (-5.40, -0.55, 3),
    (-0.55, 4.30, 5),
    (4.30, 9.15, 15),
    (9.15, 14.00, 19),
    (14.00, 18.85, 7),
    (18.85, 23.70, 1),
]

left_bounds = np.array([item[0] for item in interval_data])
right_bounds = np.array([item[1] for item in interval_data])
frequencies = np.array([item[2] for item in interval_data])
midpoints = (left_bounds + right_bounds) / 2
interval_widths = right_bounds - left_bounds
n = int(np.sum(frequencies))
h = interval_widths[0]

relative_freqs = frequencies / n
densities = relative_freqs / h
cumulative_freqs = np.cumsum(frequencies)
cumulative_relative = np.cumsum(relative_freqs)

print("ИНТЕРВАЛЬНЫЙ ВАРИАЦИОННЫЙ РЯД")
print(f"n = {n}")
print(f"k = {len(interval_data)}")
print(f"h = {h:.4f}\n")

print("№   Интервал              x_i      n_i      w_i        w_i / h")
for i, (left, right, freq) in enumerate(interval_data, start=1):
    midpoint = midpoints[i - 1]
    w = relative_freqs[i - 1]
    density = densities[i - 1]
    print(
        f"{i:>2}  [{left:>5.2f}; {right:>5.2f})   "
        f"{midpoint:>6.3f}   {freq:>4d}   {w:>7.4f}   {density:>9.4f}"
    )

modal_idx = int(np.argmax(frequencies))
fm = frequencies[modal_idx]
fm_prev = frequencies[modal_idx - 1] if modal_idx > 0 else 0
fm_next = frequencies[modal_idx + 1] if modal_idx < len(frequencies) - 1 else 0

# 1. Характеристики центра распределения
mo = left_bounds[modal_idx] + h * (fm - fm_prev) / ((fm - fm_prev) + (fm - fm_next))

median_idx = int(np.where(cumulative_freqs >= n / 2)[0][0])
s_prev = cumulative_freqs[median_idx - 1] if median_idx > 0 else 0
me = left_bounds[median_idx] + h * ((n / 2 - s_prev) / frequencies[median_idx])

# 2. Выборочное среднее
x_mean = np.sum(midpoints * frequencies) / n

# 3. Дисперсии
sum_sq = np.sum(frequencies * (midpoints - x_mean) ** 2)
d_var = sum_sq / n
s2 = sum_sq / (n - 1)

# 4. Среднеквадратические отклонения
sigma = np.sqrt(d_var)
s = np.sqrt(s2)

# 5. Коэффициент вариации
v_coeff = sigma / x_mean * 100

# 6. Доверительный интервал для среднего
t_gamma = 2.0096
delta = t_gamma * s / np.sqrt(n)
ci_left = x_mean - delta
ci_right = x_mean + delta

print("\n1. ХАРАКТЕРИСТИКИ ЦЕНТРА РАСПРЕДЕЛЕНИЯ")
print(f"Модальный интервал: [{left_bounds[modal_idx]:.2f}; {right_bounds[modal_idx]:.2f})")
print(f"Mo = {mo:.4f}")
print(f"Медианный интервал: [{left_bounds[median_idx]:.2f}; {right_bounds[median_idx]:.2f})")
print(f"Me = {me:.4f}")

print("\n2. ВЫБОРОЧНОЕ СРЕДНЕЕ")
print(f"X_bar = {x_mean:.4f}")

print("\n3. ДИСПЕРСИИ")
print(f"D = {d_var:.4f}")
print(f"S^2 = {s2:.4f}")

print("\n4. СРЕДНЕКВАДРАТИЧЕСКИЕ ОТКЛОНЕНИЯ")
print(f"sigma = {sigma:.4f}")
print(f"S = {s:.4f}")

print("\n5. КОЭФФИЦИЕНТ ВАРИАЦИИ")
print(f"V = {v_coeff:.2f}%")

print("\n6. ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ ДЛЯ СРЕДНЕГО")
print(f"t = {t_gamma}")
print(f"Δ = {delta:.4f}")
print(f"[{ci_left:.4f}; {ci_right:.4f}]")

# 7. Эмпирическая функция распределения
print("\n7. ЭМПИРИЧЕСКАЯ ФУНКЦИЯ РАСПРЕДЕЛЕНИЯ")
print(f"x < {left_bounds[0]:.2f} -> 0")
for i in range(len(interval_data)):
    print(
        f"{left_bounds[i]:.2f} <= x < {right_bounds[i]:.2f} -> "
        f"{cumulative_relative[i]:.4f}"
    )
print(f"x >= {right_bounds[-1]:.2f} -> 1.0000")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

ax1.bar(left_bounds, densities, width=h, align="edge", edgecolor="blue")
ax1.set_title("Гистограмма")
ax1.set_xlabel("x")
ax1.set_ylabel("w_i / h")
ax1.grid(True, axis="y", alpha=0.3)

ax2.plot(midpoints, frequencies, marker="o")
ax2.set_title("Полигон частот")
ax2.set_xlabel("x_i")
ax2.set_ylabel("n_i")
ax2.grid(True, alpha=0.3)

left_extension = -9.0
ecdf_x = np.concatenate(([left_extension, left_bounds[0]], left_bounds, [right_bounds[-1]]))
ecdf_y = np.concatenate(([0, 0], cumulative_relative, [1]))
step_start_x = left_bounds
step_start_y = cumulative_relative

ax3.step(ecdf_x, ecdf_y, where="post")
ax3.scatter(step_start_x, step_start_y, color="blue", s=25, zorder=3)
ax3.set_title("Эмпирическая функция распределения")
ax3.set_xlabel("x")
ax3.set_ylabel("F_n(x)")
ax3.set_ylim(-0.05, 1.05)
ax3.set_xlim(left_extension, right_bounds[-1])
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
