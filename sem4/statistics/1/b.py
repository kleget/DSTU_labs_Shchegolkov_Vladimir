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

# cumulative relative frequencies
cum_rel = []
running = 0
for x in xi:
    running += freq[x]
    cum_rel.append(running / n)

print("Task b) Empirical distribution function F(x)")
print("Piecewise form:")
print(f"x <= {xi[0]}: F(x) = 0")
for i in range(len(xi) - 1):
    print(f"{xi[i]} < x <= {xi[i + 1]}: F(x) = {cum_rel[i]:.2f}")
print(f"x > {xi[-1]}: F(x) = 1")

# Step graph
x_plot = [xi[0] - 1] + xi + [xi[-1] + 1]
y_plot = [0.0] + cum_rel + [1.0]

plt.figure(figsize=(8, 5))
plt.step(x_plot, y_plot, where="post", linewidth=2)
plt.scatter(xi, cum_rel, zorder=3)
plt.ylim(-0.05, 1.05)
plt.xlim(xi[0] - 1, xi[-1] + 1)
plt.xticks(range(xi[0], xi[-1] + 1))
plt.yticks([0, 0.05, 0.2, 0.4, 0.65, 0.9, 1.0])
plt.grid(True, linestyle="--", alpha=0.5)
plt.title("Empirical distribution function")
plt.xlabel("x")
plt.ylabel("F(x)")

output_path = os.path.join(os.path.dirname(__file__), "b_empirical_function.png")
plt.tight_layout()
plt.savefig(output_path, dpi=180)

print(f"Plot saved to: {output_path}")
