data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

sum_x = 0
for x in data:
    sum_x += x
x_bar = sum_x / n

sum_sq = 0.0
for x in data:
    sum_sq += (x - x_bar) ** 2


D = sum_sq / n  #выборочная 


S2 = sum_sq / (n - 1)  #исправленная

print("Task d) Sample and corrected variance")
print(f"x_bar = {x_bar:.4f}")
print(f"sum((xi - x_bar)^2) = {sum_sq:.4f}")
print(f"D = sum((xi - x_bar)^2) / n = {D:.4f}")
print(f"S^2 = sum((xi - x_bar)^2) / (n - 1) = {S2:.4f}")
