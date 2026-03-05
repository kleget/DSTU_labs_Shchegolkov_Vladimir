import math
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

freq = {}
for x in data:
    freq[x] = freq.get(x, 0) + 1

xi = sorted(freq.keys())
ni = [freq[x] for x in xi]

value_min = min(data)
value_max = max(data)
value_range = value_max - value_min
k_est = 1 + 3.322 * math.log10(n)
k = round(k_est)
h = value_range / k

edges = [value_min + i * h for i in range(k + 1)]
edges[-1] = value_max

interval_counts = [0] * k
for x in data:
    for i in range(k):
        left = edges[i]
        right = edges[i + 1]
        if i < k - 1: # из-за того, что range с нуля, поэтому -1
            if left <= x < right: # [x)
                interval_counts[i] += 1
                break
        else:
            if left <= x <= right:
                interval_counts[i] += 1
                break

print("Task v) Frequency polygon and histogram")
print(f"Sturges estimate k ~= {k_est:.3f}")
print(f"Chosen number of intervals k = {k}")
print(f"Interval width h = {h:.2f}")
print("Histogram intervals and frequencies:")
for i in range(k):
    lb = edges[i]
    rb = edges[i + 1]
    if i < k - 1:
        print(f"[{lb:.1f}, {rb:.1f}) -> {interval_counts[i]}")
    else:
        print(f"[{lb:.1f}, {rb:.1f}] -> {interval_counts[i]}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# полигон
axes[0].plot(xi, ni, marker="o", linewidth=2)
axes[0].set_title("Frequency polygon")
axes[0].set_xlabel("xi")
axes[0].set_ylabel("ni")
axes[0].grid(True, linestyle="--", alpha=0.5)
axes[0].set_xticks(xi)

# Гистограмма
axes[1].bar(
    edges[:-1],
    interval_counts,
    width=h,
    align="edge",
    edgecolor="black",
    linewidth=1.0,
)
axes[1].set_title("Histogram")
axes[1].set_xlabel("x")
axes[1].set_ylabel("frequency")
axes[1].grid(True, axis="y", linestyle="--", alpha=0.5)

output_path = os.path.join(os.path.dirname(__file__), "v_polygon_histogram.png")
plt.tight_layout()
plt.savefig(output_path, dpi=180)

print(f"Plot saved to: {output_path}")
