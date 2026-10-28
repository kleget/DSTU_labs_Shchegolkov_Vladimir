
"""Построение графиков по результатам экспериментов (results.json -> *.png)."""
 
import json
import matplotlib
 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
 
plt.rcParams.update({
    "font.size": 12,
    "font.family": "DejaVu Sans",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})
 
BLUE = "#2E5E8C"
ORANGE = "#D9822B"
GREEN = "#3C8C5C"
 
with open("results.json", encoding="utf-8") as f:
    data = json.load(f)
 
# --------------------------------------------------------------------------
# Рисунок 4.4 — Эффективность сжатия словаря
# --------------------------------------------------------------------------
c = data["compression"]
rates = [int(r["typo_rate"] * 100) for r in c]
before = [r["before"] for r in c]
after = [r["after"] for r in c]
 
fig, ax = plt.subplots(figsize=(8, 4.6))
x = range(len(rates))
w = 0.38
b1 = ax.bar([i - w / 2 for i in x], before, w, label="До дедупликации", color=BLUE)
b2 = ax.bar([i + w / 2 for i in x], after, w, label="После дедупликации", color=ORANGE)
ax.set_xticks(list(x))
ax.set_xticklabels([f"{r}%" for r in rates])
ax.set_xlabel("Доля слов с опечатками в исходном тексте")
ax.set_ylabel("Количество уникальных слов в словаре")
ax.set_title("Сокращение размера словаря после дедуплика-ции")
ax.legend()
for rect in list(b1) + list(b2):
    ax.annotate(str(int(rect.get_height())),
                (rect.get_x() + rect.get_width() / 2, rect.get_height()),
                textcoords="offset points", xytext=(0, 3),
                ha="center", fontsize=9)
fig.savefig("fig_compression.png")
plt.close(fig)
 
# --------------------------------------------------------------------------
# Рисунок 4.5 — Время работы: наивный перебор vs оптими-зированный
# --------------------------------------------------------------------------
p = data["performance"]
sizes = [r["dict_size"] for r in p]
t_naive = [r["time_naive_ms"] for r in p]
t_opt = [r["time_opt_ms"] for r in p]
 
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(sizes, t_naive, "o-", color=BLUE, linewidth=2,
        label="Наивный перебор всех пар, O(n²)")
ax.plot(sizes, t_opt, "s-", color=GREEN, linewidth=2,
        label="С группировкой по длине и префиксу (DSU)")
ax.set_xlabel("Размер исходного словаря (число уникальных слов)")
ax.set_ylabel("Время выполнения, мс")
ax.set_title("Время дедупликации в зависимости от размера словаря")
ax.set_yscale("log")
ax.legend()
for xi, yi in zip(sizes, t_naive):
    ax.annotate(f"{yi:.0f}", (xi, yi), textcoords="offset points",
                xytext=(0, 7), ha="center", fontsize=8, color=BLUE)
for xi, yi in zip(sizes, t_opt):
    ax.annotate(f"{yi:.0f}", (xi, yi), textcoords="offset points",
                xytext=(0, -14), ha="center", fontsize=8, color=GREEN)
fig.savefig("fig_time.png")
plt.close(fig)
 
# --------------------------------------------------------------------------
# Рисунок 4.6 — Число сравнений (вызовов Левенштейна)
# --------------------------------------------------------------------------
cmp_naive = [r["cmp_naive"] for r in p]
cmp_opt = [r["cmp_opt"] for r in p]
 
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(sizes, cmp_naive, "o-", color=BLUE, linewidth=2,
        label="Наивный перебор всех пар")
ax.plot(sizes, cmp_opt, "s-", color=GREEN, linewidth=2,
        label="С группировкой по бакетам")
ax.set_xlabel("Размер исходного словаря (число уникальных слов)")
ax.set_ylabel("Количество вычислений расстояния Левен-штейна")
ax.set_title("Число сравнений слов: влияние группировки по бакетам")
ax.set_yscale("log")
ax.legend()
fig.savefig("fig_comparisons.png")
plt.close(fig)
 
# --------------------------------------------------------------------------
# Рисунок 4.7 — Ускорение (во сколько раз быстрее)
# --------------------------------------------------------------------------
speedup = [r["speedup"] for r in p]
 
fig, ax = plt.subplots(figsize=(8, 4.6))
bars = ax.bar([str(s) for s in sizes], speedup, color=ORANGE, width=0.6)
ax.set_xlabel("Размер исходного словаря (число уникальных слов)")
ax.set_ylabel("Ускорение, раз")
ax.set_title("Во сколько раз оптимизированный алгоритм быстрее наивного")
for rect in bars:
    ax.annotate(f"{rect.get_height():.0f}×",
                (rect.get_x() + rect.get_width() / 2, rect.get_height()),
                textcoords="offset points", xytext=(0, 3),
                ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0, max(speedup) * 1.15)
fig.savefig("fig_speedup.png")
plt.close(fig)
 
# --------------------------------------------------------------------------
# Рисунок 4.8 — Влияние порога расстояния Левенштейна
# --------------------------------------------------------------------------
t = data["threshold"]
dists = [r["max_dist"] for r in t]
after_t = [r["after"] for r in t]
merged_t = [r["merged"] for r in t]
 
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(dists, after_t, "o-", color=BLUE, linewidth=2,
        label="Уникальных слов после дедупликации")
ax.plot(dists, merged_t, "s-", color=ORANGE, linewidth=2,
        label="Количество выполненных склеек")
ax.set_xlabel("Максимально допустимое расстояние Левен-штейна")
ax.set_ylabel("Количество слов")
ax.set_title("Влияние порога расстояния на результат де-дупликации")
ax.set_xticks(dists)
ax.legend()
ax.axvspan(1.5, 2.5, color=GREEN, alpha=0.12)
ax.annotate("оптимальный\nдиапазон", (2, max(after_t) * 0.75),
            ha="center", fontsize=10, color=GREEN)
fig.savefig("fig_threshold.png")
plt.close(fig)
 
print("Графики построены:")
for name in ("fig_compression", "fig_time", "fig_comparisons",
             "fig_speedup", "fig_threshold"):
    print(" ", name + ".png")
 
