data = [17, 18, 16, 16, 17, 18, 19, 17, 15, 17, 19, 18, 16, 16, 18, 18, 12, 17, 15, 15]
n = len(data)

# Manual statistical distribution
freq = {}
for x in data:
    freq[x] = freq.get(x, 0) + 1

xi = sorted(freq.keys())

print("Statistical distribution of the sample")
print(f"n = {n}")
print(f"raw data: {data}")
print(f"sorted data: {sorted(data)}")
print()
print("xi\tni\tpi\tNi\tFi")

cumulative_count = 0
for x in xi:
    ni = freq[x]
    pi = ni / n
    cumulative_count += ni
    fi = cumulative_count / n
    print(f"{x}\t{ni}\t{pi:.2f}\t{cumulative_count}\t{fi:.2f}")
