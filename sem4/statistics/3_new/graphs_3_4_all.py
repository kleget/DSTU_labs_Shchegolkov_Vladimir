import numpy as np
import matplotlib.pyplot as plt
 
# ============================================================
# Графики для тетради:
# 1) гистограмма интервального ряда
# 2) Колмогоров: Fn и F0 для нормального распределения
# 3) Колмогоров: Fn и F0 для равномерного распределения
# ============================================================

# -----------------------------
# Общие данные
# -----------------------------

intervals = [
    "[-5.4; -1.2]",
    "(-1.2; 3.0]",
    "(3.0; 7.2]",
    "(7.2; 11.4]",
    "(11.4; 15.6]",
    "(15.6; 19.8]",
    "(19.8; 24.0]"
]

freq = np.array([2, 5, 7, 19, 14, 2, 1])

x = np.array([-1.2, 3.0, 7.2, 11.4, 15.6, 19.8, 24.0])

# Эмпирическая функция распределения
F_n = np.array([0.04, 0.14, 0.28, 0.66, 0.94, 0.98, 1.00])

# Теоретическая функция нормального распределения
F_0_norm = np.array([0.0309, 0.1342, 0.3648, 0.6610, 0.8803, 0.9736, 0.9965])

# Теоретическая функция равномерного распределения
F_0_uniform = np.array([0.1429, 0.2857, 0.4286, 0.5714, 0.7143, 0.8571, 1.0000])


# -----------------------------
# График 3: гистограмма интервального ряда
# -----------------------------

plt.figure(figsize=(10, 5))
plt.bar(intervals, freq, edgecolor="black")

plt.title("Гистограмма интервального ряда")
plt.xlabel("Интервалы")
plt.ylabel("Частота n_i")
plt.xticks(rotation=30)
plt.grid(axis="y", alpha=0.4)

plt.tight_layout()
plt.savefig("graph_3_histogram.png", dpi=300)
plt.show()


# -----------------------------
# График 4.1: Колмогоров, нормальное распределение
# -----------------------------

plt.figure(figsize=(8, 5))
plt.plot(x, F_n, marker="o", label="F_n(x), эмпирическая")
plt.plot(x, F_0_norm, marker="o", label="F_0(x), нормальная")

plt.title("Колмогоров: сравнение с нормальным распределением")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.grid(True, alpha=0.4)
plt.legend()

plt.tight_layout()
plt.savefig("graph_4_kolmogorov_normal.png", dpi=300)
plt.show()


# -----------------------------
# График 4.2: Колмогоров, равномерное распределение
# -----------------------------

plt.figure(figsize=(8, 5))
plt.plot(x, F_n, marker="o", label="F_n(x), эмпирическая")
plt.plot(x, F_0_uniform, marker="o", label="F_0(x), равномерная")

plt.title("Колмогоров: сравнение с равномерным распределением")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.grid(True, alpha=0.4)
plt.legend()

plt.tight_layout()
plt.savefig("graph_4_kolmogorov_uniform.png", dpi=300)
plt.show()


print("Графики сохранены:")
print("graph_3_histogram.png")
print("graph_4_kolmogorov_normal.png")
print("graph_4_kolmogorov_uniform.png")
