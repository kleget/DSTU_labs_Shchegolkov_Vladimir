import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2
from math import exp, factorial

# Вариант 13.
# В листе написано n = 200, но частоты дают сумму 159:
# 62 + 45 + 22 + 16 + 8 + 4 + 2 = 159.
# Поэтому в расчетах берем n как сумму наблюдаемых частот.

x = np.array([0, 1, 2, 3, 4, 5, 6])
n_i = np.array([62, 45, 22, 16, 8, 4, 2])

alpha = 0.05
n = n_i.sum()

# Оценка параметра λ для распределения Пуассона:
# λ = среднее значение X по выборке.
lam = (x * n_i).sum() / n

print(f"Объем выборки n = {n}")
print(f"Оценка λ = {lam:.4f}")

def poisson_p(k, lam):
    """Вероятность P(X = k) для распределения Пуассона."""
    return exp(-lam) * lam**k / factorial(k)

p_i = np.array([poisson_p(k, lam) for k in x])
theor_i = n * p_i

raw_table = pd.DataFrame({
    "x_i": x,
    "n_i": n_i,
    "p_i": p_i,
    "теор_частота": theor_i
})

print("\nТаблица до объединения:")
print(raw_table.round(4))

# По замечанию преподавателя объединяем группы с маленькими частотами.
# У нас n_i = 4 и n_i = 2 слишком маленькие, а также теоретическая частота
# для x=4 меньше 5, поэтому удобно объединить хвост: x >= 4.
groups = ["0", "1", "2", "3", ">=4"]

obs = np.array([
    n_i[0],
    n_i[1],
    n_i[2],
    n_i[3],
    n_i[4:].sum()
])

p = np.array([
    poisson_p(0, lam),
    poisson_p(1, lam),
    poisson_p(2, lam),
    poisson_p(3, lam),
    1 - sum(poisson_p(k, lam) for k in range(4))
])

exp_freq = n * p
chi_parts = (obs - exp_freq) ** 2 / exp_freq
chi_emp = chi_parts.sum()

# Степени свободы:
# k - число групп после объединения,
# 1 - из-за условия суммы вероятностей,
# 1 - потому что λ оценивали по выборке.
df = len(groups) - 1 - 1

chi_crit = chi2.ppf(1 - alpha, df)
p_value = 1 - chi2.cdf(chi_emp, df)

result_table = pd.DataFrame({
    "группа": groups,
    "набл_частота": obs,
    "вероятность": p,
    "теор_частота": exp_freq,
    "вклад_в_chi2": chi_parts
})

print("\nТаблица после объединения:")
print(result_table.round(4))

print(f"\nχ² эмпирическое = {chi_emp:.4f}")
print(f"χ² критическое = {chi_crit:.4f}")
print(f"Степени свободы = {df}")
print(f"p-value = {p_value:.6f}")

if chi_emp < chi_crit:
    print("Вывод: гипотеза о распределении Пуассона не отвергается.")
else:
    print("Вывод: гипотеза о распределении Пуассона отвергается.")

# График для отчета
idx = np.arange(len(groups))
width = 0.38

plt.figure(figsize=(8, 4.8))
plt.bar(idx - width / 2, obs, width, label="Наблюдаемая частота")
plt.bar(idx + width / 2, exp_freq, width, label="Теоретическая частота")
plt.xticks(idx, groups)
plt.xlabel("Группа значений X")
plt.ylabel("Частота")
plt.title("Вариант 13: наблюдаемые и теоретические частоты")
plt.legend()
plt.tight_layout()
plt.savefig("variant13_poisson_plot.png", dpi=200)
plt.show()
