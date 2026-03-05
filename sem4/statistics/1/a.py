data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

sorted_data = sorted(data)
value_min = sorted_data[0]
value_max = sorted_data[-1]
value_range = value_max - value_min

freq = {} #frequency-частота
for x in sorted_data:
    freq[x] = freq.get(x, 0) + 1

max_freq = max(freq.values())
modes = []
for x in sorted(freq.keys()):
    if freq[x] == max_freq:
        modes.append(x)

if n % 2 == 1:
    median = sorted_data[n // 2]
else:
    median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

print("Task a) Characteristics of variation series")
print(f"n = {n}")
print(f"sorted data: {sorted_data}")
print(f"range R = Xmax - Xmin = {value_max} - {value_min} = {value_range}")
print(f"mode(s) = {modes}")
print(f"median = {median}")
