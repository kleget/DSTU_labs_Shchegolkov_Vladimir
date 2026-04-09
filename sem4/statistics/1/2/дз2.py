import matplotlib.pyplot as plt
import numpy as np

interval_data = [
    (-2.3, 1.7, 2),
    (1.7, 5.6, 10),
    (5.6, 9.6, 15),
    (9.6, 13.6, 13),
    (13.6, 17.5, 5),
    (17.5, 21.5, 5)
]

left_bounds = np.array([item[0] for item in interval_data])
right_bounds = np.array([item[1] for item in interval_data])
frequencies = np.array([item[2] for item in interval_data])

midpoints = (left_bounds + right_bounds) / 2

n = np.sum(frequencies)

relative_freqs = frequencies / n

interval_widths = right_bounds - left_bounds

if not np.allclose(interval_widths, interval_widths[0]):
    print("ВНИМАНИЕ: Интервалы имеют разную ширину!")
h = interval_widths[0]
densities = relative_freqs / h

print("ИНТЕРВАЛЬНЫЙ ВАРИАЦИОННЫЙ РЯД")
print(f"Объем выборки: n = {n}")
print(f"Количество интервалов: k = {len(interval_data)}")
print(f"Длина интервала: h = {h:.4f}\n")

print("Интервальный ряд:")
print("№  Интервал    Середина  Частота(n_i)  Отн.частота(w_i)  Плотность(w_i/h)")

for i, (left, right, freq) in enumerate(interval_data, 1):
    w = relative_freqs[i-1]
    density = densities[i-1]
    midpoint = midpoints[i-1]
    print(f"{i:2d} [{left:.1f};{right:.1f})   {midpoint:6.2f}    {freq:6d}        {w:.4f}          {density:.4f}")

print("1. ХАРАКТЕРИСТИКИ ЦЕНТРА РАСПРЕДЕЛЕНИЯ")

modal_idx = np.argmax(frequencies)
if modal_idx == 0:
    # первый интервал
    mo = left_bounds[modal_idx] + h * (frequencies[modal_idx] - 0) / \
         ((frequencies[modal_idx] - 0) + (frequencies[modal_idx] - frequencies[modal_idx + 1]))
elif modal_idx == len(frequencies) - 1:
    # последний интервал
    mo = left_bounds[modal_idx] + h * (frequencies[modal_idx] - frequencies[modal_idx - 1]) / \
         ((frequencies[modal_idx] - frequencies[modal_idx - 1]) + (frequencies[modal_idx] - 0))
else:
    # остальные интервалы
    mo = left_bounds[modal_idx] + h * (frequencies[modal_idx] - frequencies[modal_idx - 1]) / \
         ((frequencies[modal_idx] - frequencies[modal_idx - 1]) + (frequencies[modal_idx] - frequencies[modal_idx + 1]))

print(f"Модальный интервал: [{left_bounds[modal_idx]:.1f};{right_bounds[modal_idx]:.1f})")
print(f"Мода Mo = {mo:.4f}")

# Медиана
cumulative_freqs = np.cumsum(frequencies)
median_idx = np.where(cumulative_freqs >= n/2)[0][0]

if median_idx == 0:
    s_prev = 0
else:
    s_prev = cumulative_freqs[median_idx - 1]

me = left_bounds[median_idx] + h * ((n/2 - s_prev) / frequencies[median_idx])
print(f"Медианный интервал: [{left_bounds[median_idx]:.1f};{right_bounds[median_idx]:.1f})")
print(f"Медиана Me = {me:.4f}")

print("2. ВЫБОРОЧНОЕ СРЕДНЕЕ")

x_mean = np.sum(midpoints * frequencies) / n
print(f"Среднее арифметическое (по серединам интервалов):")
print(f"X̄ = {x_mean:.4f}")

print("3. ДИСПЕРСИИ")

d_var = np.sum(frequencies * (midpoints - x_mean) ** 2) / n

s2 = np.sum(frequencies * (midpoints - x_mean) ** 2) / (n - 1) if n > 1 else 0

print(f"Выборочная дисперсия Dв = {d_var:.4f}")
print(f"Исправленная дисперсия S² = {s2:.4f}")

print("4. СРЕДНЕКВАДРАТИЧЕСКИЕ ОТКЛОНЕНИЯ")

sigma = np.sqrt(d_var) if d_var >= 0 else 0
s = np.sqrt(s2) if s2 >= 0 else 0

print(f"Выборочное СКО σ = {sigma:.4f}")
print(f"Исправленное СКО S = {s:.4f}")

print("5. КОЭФФИЦИЕНТ ВАРИАЦИИ")

V = (sigma / x_mean) * 100 if x_mean != 0 else 0
print(f"Коэффициент вариации V = {V:.2f}%")

print("6. ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ ДЛЯ СРЕДНЕГО")

gamma = 0.95
if n > 1 and s > 0:
    t_gamma = 1.7291  # для n-1 = 19 при надежности 0.95
    
    delta = t_gamma * s / np.sqrt(n)
    lower_bound = x_mean - delta
    upper_bound = x_mean + delta
    
    print(f"Надежность: {gamma}")
    print(f"Квантиль Стьюдента t({gamma}, {n-1}) = {t_gamma}")
    print(f"Предельная ошибка: {delta:.4f}")
    print(f"Доверительный интервал: ({lower_bound:.4f}; {upper_bound:.4f})")
else:
    print("Недостаточно данных для расчета доверительного интервала")

print("7. ЭМПИРИЧЕСКАЯ ФУНКЦИЯ РАСПРЕДЕЛЕНИЯ")

cumulative_relative = np.cumsum(relative_freqs)
print("x        F*(x)")
print(f"x < {left_bounds[0]:.1f}    0.0000")
for i in range(len(interval_data)):
    if i < len(interval_data) - 1:
        print(f"{left_bounds[i]:.1f} ≤ x < {left_bounds[i+1]:.1f}    {cumulative_relative[i]:.4f}")
    else:
        print(f"x ≥ {right_bounds[i]:.1f}    {cumulative_relative[i]:.4f}")

print("8. ГРАФИЧЕСКОЕ ПРЕДСТАВЛЕНИЕ")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle(f'Интервальный вариационный ряд (n={n}, k={len(interval_data)}, h={h:.2f})', fontsize=14)

ax1.bar(left_bounds, densities, width=h, 
        edgecolor='black', align='edge',
        color='lightblue', alpha=0.7)
ax1.set_xlabel('Значения признака')
ax1.set_ylabel('Плотность относительной частоты (w_i/h)')
ax1.set_title('Гистограмма распределения')
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_xticks(left_bounds)
ax1.set_xticklabels([f'{b:.1f}' for b in left_bounds])

ax2.plot(midpoints, frequencies, 'ro-', linewidth=2, markersize=8, label='Полигон частот')
ax2.set_xlabel('Середины интервалов')
ax2.set_ylabel('Частоты n_i')
ax2.set_title('Полигон частот')
ax2.grid(True, alpha=0.3)
ax2.legend()

ax3.plot(midpoints, cumulative_relative, 'gs-', linewidth=2, markersize=8, label='Кумулята')
ax3.set_xlabel('Середины интервалов')
ax3.set_ylabel('Накопленные относительные частоты')
ax3.set_title('Кумулятивная кривая')
ax3.grid(True, alpha=0.3)
ax3.set_ylim(-0.05, 1.05)
ax3.legend()

for i, (x, y) in enumerate(zip(midpoints, cumulative_relative)):
    ax3.annotate(f'{y:.3f}', (x, y), xytext=(5, 5), 
                textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.show()

print("\nПрограмма завершена!")