data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]

# Statistical distribution (xi, ni)
freq = {}
for x in data:
    freq[x] = freq.get(x, 0) + 1

xi = sorted(freq.keys())
ni = [freq[x] for x in xi]

weighted_sum = 0
for i in range(len(xi)):
    weighted_sum += xi[i] * ni[i]

n = 0
for count in ni:
    n += count

x_bar = weighted_sum / n

numerator_formula = " + ".join(f"{xi[i]}*{ni[i]}" for i in range(len(xi)))

print("Task g) Sample mean")
print("Using grouped-data formula: x_bar = sum(xi*ni) / sum(ni)")
print(f"xi: {xi}")
print(f"ni: {ni}")
print(f"sum(xi*ni) = {numerator_formula} = {weighted_sum}")
print(f"sum(ni) = {n}")
print(f"x_bar = {weighted_sum} / {n} = {x_bar:.4f}")
