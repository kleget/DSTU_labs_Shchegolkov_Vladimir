import random
import time

# 1. Сортировка прямым включением (Insertion Sort)
def insertion_sort(arr):
    comparisons = assignments = 0
    for i in range(1, len(arr)):
        key = arr[i]
        assignments += 1
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                assignments += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
        assignments += 1
    return comparisons, assignments

# 2. Сортировка прямым выбором (Selection Sort)
def selection_sort(arr):
    comparisons = assignments = 0
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            assignments += 3
    return comparisons, assignments

# 3. Сортировка пузырьком
def bubble_sort(arr):
    comparisons = assignments = 0
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                assignments += 3
    return comparisons, assignments

# 4. Быстрая сортировка (Quick Sort)
def quick_sort(arr):
    comparisons = assignments = 0
    
    def _quick_sort(items, left, right):
        nonlocal comparisons, assignments
        if left < right:
            pivot_index = partition(items, left, right)
            _quick_sort(items, left, pivot_index - 1)
            _quick_sort(items, pivot_index + 1, right)
    
    def partition(items, left, right):
        nonlocal comparisons, assignments
        pivot = items[(left + right) // 2]
        assignments += 1
        i = left - 1
        j = right + 1
        
        while True:
            i += 1
            while True:
                comparisons += 1
                if items[i] >= pivot:
                    break
                i += 1
            
            j -= 1
            while True:
                comparisons += 1
                if items[j] <= pivot:
                    break
                j -= 1
            
            if i >= j:
                return j
            
            items[i], items[j] = items[j], items[i]
            assignments += 3
    
    _quick_sort(arr, 0, len(arr) - 1)
    return comparisons, assignments

# Генерация тестовых данных
def generate_array(size, array_type='random'):
    if array_type == 'random':
        return [random.randint(1, 10000) for _ in range(size)]
    elif array_type == 'sorted':
        return list(range(1, size + 1))
    elif array_type == 'reverse':
        return list(range(size, 0, -1))
    elif array_type == 'partially_sorted':
        sorted_part = size // 2
        return list(range(1, sorted_part + 1)) + [random.randint(1, 10000) for _ in range(size - sorted_part)]

# Основная программа
def main():
    algorithms = {
        '1': ('Прямое включение', insertion_sort),
        '2': ('Прямой выбор', selection_sort),
        '3': ('Прямой обмен', bubble_sort),
        '4': ('Быстрая сортировка', quick_sort)
    }
    
    while True:
        print("\n" + "="*50)
        print("Лабораторная работа 4: Методы сортировки")
        print("="*50)
        print("1. Сортировка одного массива")
        print("2. Сравнение всех алгоритмов")
        print("3. Выход")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            size = int(input("Размер массива: "))
            arr_type = input("Тип массива (random/sorted/reverse/partially_sorted): ")
            
            arr = generate_array(size, arr_type)
            print(f"\nИсходный массив: {arr if size <= 20 else arr[:10]}...")
            
            print("\nВыберите алгоритм:")
            for key, (name, _) in algorithms.items():
                print(f"{key}. {name}")
            
            algo_choice = input("Ваш выбор: ")
            
            if algo_choice in algorithms:
                name, func = algorithms[algo_choice]
                test_arr = arr.copy()
                
                start_time = time.time()
                comparisons, assignments = func(test_arr)
                end_time = time.time()
                
                print(f"\n{name}:")
                print(f"Отсортированный массив: {test_arr if size <= 20 else test_arr[:10]}...")
                print(f"Время: {end_time - start_time:.6f} сек")
                print(f"Сравнения: {comparisons}")
                print(f"Присваивания: {assignments}")
        
        elif choice == '2':
            sizes = [20, 500, 1000, 3000, 5000, 10000]
            array_types = ['random', 'sorted', 'reverse', 'partially_sorted']
            
            for size in sizes:
                print(f"\n--- Размер: {size} ---")
                for arr_type in array_types:
                    arr = generate_array(size, arr_type)
                    print(f"\nТип: {arr_type}")
                    
                    results = []
                    for name, func in algorithms.values():
                        test_arr = arr.copy()
                        start_time = time.time()
                        comparisons, assignments = func(test_arr)
                        end_time = time.time()
                        
                        results.append((name, end_time - start_time, comparisons, assignments))
                    
                    # Сортировка по времени
                    results.sort(key=lambda x: x[1])
                    
                    print(f"{'Алгоритм':<20} {'Время':<10} {'Сравнения':<12} {'Присваивания':<12}")
                    for name, time_taken, comp, assign in results:
                        print(f"{name:<20} {time_taken:<10.6f} {comp:<12} {assign:<12}")
        
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
