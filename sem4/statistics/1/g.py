data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

sum_x = 0
for x in data:
    sum_x += x

x_bar = sum_x / n

print("Task g) Sample mean")
print(f"sum(xi) = {sum_x}")
print(f"x_bar = sum(xi) / n = {sum_x} / {n} = {x_bar:.4f}")
