import math

data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)
gamma = 0.95
alpha = 1 - gamma

sum_x = 0
for x in data:
    sum_x += x
x_bar = sum_x / n

sum_sq = 0.0
for x in data:
    sum_sq += (x - x_bar) ** 2

# corrected standard deviation
S2 = sum_sq / (n - 1)
s = math.sqrt(S2)

# t_{alpha/2, n-1} for alpha=0.05, df=19 from Student table
t_crit = 2.093

std_error = s / math.sqrt(n)
delta = t_crit * std_error
left = x_bar - delta
right = x_bar + delta

print("Task z) 95% confidence interval for mean")
print(f"gamma = {gamma}, alpha = {alpha}")
print(f"n = {n}, df = {n - 1}")
print(f"x_bar = {x_bar:.4f}")
print(f"s = {s:.4f}")
print(f"t_crit = {t_crit}")
print(f"std_error = s / sqrt(n) = {std_error:.4f}")
print(f"delta = t_crit * std_error = {delta:.4f}")
print(f"confidence interval: ({left:.4f}; {right:.4f})")
