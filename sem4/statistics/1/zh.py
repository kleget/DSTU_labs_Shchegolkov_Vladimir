import math

data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

sum_x = 0
for x in data:
    sum_x += x
x_bar = sum_x / n

sum_sq = 0.0
for x in data:
    sum_sq += (x - x_bar) ** 2

S2 = sum_sq / (n - 1)
s = math.sqrt(S2)


V = (s / x_bar) * 100

print("Task zh) Coefficient of variation (%)")
print(f"x_bar = {x_bar:.4f}")
print(f"s = {s:.4f}")
print(f"V = (s / x_bar) * 100% = {V:.2f}%")
