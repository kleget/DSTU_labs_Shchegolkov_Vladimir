import random
import time

def linear_search(arr, target):
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons

def linear_search_barrier(arr, target):
    comparisons = 0
    arr.append(target)  # Добавляем барьер
    i = 0
    while arr[i] != target:
        comparisons += 1
        i += 1
    arr.pop()  # Убираем барьер
    return i if i < len(arr) else -1, comparisons + 1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    comparisons = 0
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons

# Основной тест
sizes = [100, 500, 1000, 3000, 10000]
print("Размер | Линейный | Барьер | Бинарный")
print("------ | -------- | ------ | --------")

for size in sizes:
    arr = sorted(random.sample(range(size * 10), size))
    
    linear_time = binary_time = barrier_time = 0
    linear_comp = binary_comp = barrier_comp = 0
    
    for _ in range(10):
        target = random.choice(arr)
        
        start = time.time()
        pos, comp = linear_search(arr, target)
        linear_time += time.time() - start
        linear_comp += comp
        
        start = time.time()
        pos, comp = linear_search_barrier(arr.copy(), target)
        barrier_time += time.time() - start
        barrier_comp += comp
        
        start = time.time()
        pos, comp = binary_search(arr, target)
        binary_time += time.time() - start
        binary_comp += comp
    
    print(f"{size:6} | {linear_time/10:.4f} | {barrier_time/10:.4f} | {binary_time/10:.4f}")

# Дополнительно: сравнение количества сравнений
print("\nСреднее количество сравнений:")
print("Размер | Линейный | Барьер | Бинарный")
for size in sizes:  
    arr = sorted(random.sample(range(size * 10), size))
    linear_comp = barrier_comp = binary_comp = 0
    
    for _ in range(10):
        target = random.choice(arr)
        _, comp = linear_search(arr, target)
        linear_comp += comp
        
        _, comp = linear_search_barrier(arr.copy(), target)
        barrier_comp += comp
        
        _, comp = binary_search(arr, target)
        binary_comp += comp
    
    print(f"{size:6} | {linear_comp/10:8.1f} | {barrier_comp/10:6.1f} | {binary_comp/10:8.1f}")