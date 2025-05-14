import numpy as np

# 1
arr1 = np.arange(1, 11)
arr1_2d = arr1.reshape(2, 5)  # Преобразование в 2x5

# 2
a = np.random.randint(0, 10, (3, 3))
b = np.random.randint(0, 10, (3, 3))
sum_ab = a + b  # Поэлементное сложение

# 3
arr3 = np.random.randint(0, 16, (4, 4))
slice_cols = arr3[:, 1:3]  # Срез столбцов 1 и 2 (индексация с 0)

# 4
arr4 = np.random.rand(10)
mean4 = np.mean(arr4)

# 5
arr5 = np.random.rand(5, 5)
max_val = arr5.max()
min_val = arr5.min()
max_idx = np.unravel_index(arr5.argmax(), arr5.shape)
min_idx = np.unravel_index(arr5.argmin(), arr5.shape)

# 6
arr6 = np.array([1, 2, 2, 3, 4, 4, 5])
unique_arr6 = np.unique(arr6)  # Уникальные значения

# 7
arr7 = np.random.randint(0, 101, 20)
filtered7 = arr7[arr7 > 50]

# 8
m1 = np.random.randint(0, 5, (2, 2))
m2 = np.random.randint(0, 5, (2, 2))
product = np.dot(m1, m2)
det = np.linalg.det(product)

# 9
n, m = 5, 6
mat9 = np.zeros((n, m))
mat9[[0, -1], :] = 1  # Первая и последняя строки
mat9[:, [0, -1]] = 1  # Первый и последний столбцы

# 10
mat10 = np.random.randint(0, 10, (4, 4))  # Квадратная матрица
diag_sum = np.trace(mat10)

# 11
vec11 = np.array([0, 5, 0, 3, 0])
nonzero_indices = np.nonzero(vec11)[0]

# 12
vec12 = np.array([2, 4, 5, 7, 9, 1])
vec12[(vec12 > 3) & (vec12 < 8)] *= -1

# 13
vec13_sorted = np.sort(vec12)  # По возрастанию

# 14
a = np.array([1, 2, 3, 4, 5])
b = np.array([3, 4, 5, 6, 7])
common = np.intersect1d(a, b)  # Общие элементы
count_common = common.size  # Считаем кол-во

# 15
arr15 = np.array([3, 5, 7, 9, 10, 12])
selected = arr15[(arr15 >= 5) & (arr15 <= 10)]  # Фильтр