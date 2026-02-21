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

D = sum_sq / n #выборочное
S2 = sum_sq / (n - 1) #исправленное

sigma = math.sqrt(D)
s = math.sqrt(S2)

print("Task e) Sample and corrected standard deviations")
print(f"sqrt(D) = sqrt({D:.4f}) = {sigma:.4f}")
print(f"sqrt(S^2) = sqrt({S2:.4f}) = {s:.4f}")
