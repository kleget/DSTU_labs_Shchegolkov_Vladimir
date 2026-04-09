import numpy as np

raw_data = [16.8, 2.6, 11.6, 2.7, 18.7, 6.4, 10.5, 2.7, -1.3, 4.0, 
            4.8, 10.7, 5.9, 4.9, 9.4, 8.4, 7.3, 9.8, 5.5, 12.6, 
            7.1, 10.8, 3.1, 10.2, 9.4, 9.4, 10.4, 14.5, 12.5, 15.1, 
            3.8, 16.9, 8.3, 6.9, 6.0, 19.9, 18.3, 12.8, 21.5, 12.4, 
            7.0, 8.1, 4.7, 11.9, -2.3, 9.2, 18.2, 7.1, 16.7, 11.4]

k = int(1 + np.log2(len(raw_data)))
print(f"Рекомендуемое количество интервалов: {k}")

min_val = min(raw_data)
max_val = max(raw_data)
interval_width = (max_val - min_val) / k

bins = np.linspace(min_val, max_val, k + 1)
hist, bin_edges = np.histogram(raw_data, bins=bins)

interval_data = []
for i in range(len(hist)):
    left = round(bin_edges[i], 2)
    right = round(bin_edges[i+1], 2)
    freq = hist[i]
    interval_data.append((left, right, freq))
    
print("\nинтервальный ряд:")
for interval in interval_data:
    print(f"    ({interval[0]:.1f}, {interval[1]:.1f}, {interval[2]})")