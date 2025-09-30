import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.gridspec import GridSpec

# 1-2. Построение нормального распределения и его приближения
mu = 7.5 - 4  # Среднее значение
sigma = 1     # Стандартное отклонение (выбрано произвольно)
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)  # Диапазон значений x
f = 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-(x - mu)**2 / (2*sigma**2))  # Формула нормального распределения

plt.figure()
plt.plot(x, f, 'b-', label='Нормальное распределение')
plt.plot(x, f + np.random.normal(0, 0.005, len(x)), 'r--', label='Приближение')  # Добавляем шум для имитации приближения
plt.title('Нормальное распределение и приближение')
plt.xlabel('x')
plt.ylabel('Плотность вероятности')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Детальная сетка
plt.legend()  # Легенда для различия графиков
plt.show()

# 3. 10 графиков белого шума (случайные значения в диапазоне [-1, 1])
plt.figure()
for _ in range(10):
    y = np.random.uniform(-1, 1, 100)  # Генерация случайных значений
    plt.plot(y, alpha=0.5)  # alpha для прозрачности линий
plt.title('Графики белого шума')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.grid(True)
plt.show()

# 4. Работа с CSV и построение диаграмм
# Создаем данные для CSV-файла
data = [
    ['Сон', 8],
    ['Учеба', 6],
    ['Еда', 2],
    ['Отдых', 4],
    ['Спорт', 2]
]

# Записываем данные в CSV
with open('schedule.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Мероприятие', 'Время'])  # Заголовок
    writer.writerows(data)  # Данные

# Чтение данных из CSV
activities = []
time = []
with open('schedule.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Пропускаем заголовок
    for row in reader:
        activities.append(row[0])
        time.append(int(row[1]))

# Столбчатая диаграмма
plt.figure()
plt.bar(activities, time)
plt.title('Распорядок дня (столбчатая диаграмма)')
plt.ylabel('Часы')
plt.xticks(rotation=45)  # Поворот подписей для удобства
plt.tight_layout()  # Автоматическая настройка layout
plt.show()

# Круговая диаграмма с процентами
plt.figure()
plt.pie(time, labels=activities, autopct='%1.1f%%')  # autopct для отображения процентов
plt.title('Распорядок дня (круговая диаграмма)')
plt.tight_layout()
plt.show()

# 5. Гистограмма и boxplot для нормального распределения
data_normal = np.random.normal(0, 1, 1000)  # Генерация данных
plt.figure(figsize=(10, 4))
plt.subplot(121)  # 1 строка, 2 столбца, 1 график
plt.hist(data_normal, bins=30, edgecolor='k')  # Гистограмма с 30 корзинами
plt.title('Гистограмма нормального распределения')
plt.subplot(122)  # 1 строка, 2 столбца, 2 график
plt.boxplot(data_normal)  # Boxplot
plt.title('Boxplot нормального распределения')
plt.savefig('histogram.png')  # Сохранение гистограммы
plt.show()

# 6. График кривой: x² - 3xy + y² + x + 2y +5 = 0
x = np.linspace(-5, 5, 400)
y = np.linspace(-5, 5, 400)
X, Y = np.meshgrid(x, y)  # Создаем сетку для построения
Z = X**2 - 3*X*Y + Y**2 + X + 2*Y + 5  # Уравнение кривой
plt.figure()
plt.contour(X, Y, Z, levels=[0], colors='b')  # Рисуем линию уровня Z=0
plt.title('Кривая: $x^2 - 3xy + y^2 + x + 2y +5 = 0$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

# 7. Четыре функции и их графики в subplots
def f1(x): return x + 3        # Линейная
def f2(x): return x**2         # Квадратичная
def f3(x): return x**3         # Кубическая
def f4(x): return x**4         # Четвертой степени
L = [f1, f2, f3, f4]  # Список функций

x = np.linspace(-3, 3, 100)
plt.figure(figsize=(10, 8))
for i, func in enumerate(L, 1):  # enumerate для нумерации
    plt.subplot(2, 2, i)  # 2 строки, 2 столбца
    plt.plot(x, func(x))
    plt.title(f'Функция {i}')
plt.tight_layout()  # Улучшает расположение подграфиков
plt.show()

# 8. Scatter-plot для матрицы 50x2
matrix = np.random.randint(0, 100, (50, 2))  # Случайная матрица
colors = ['red' if i % 2 == 0 else 'blue' for i in range(50)]  # Четные - красные, нечетные - синие
plt.figure()
plt.scatter(matrix[:, 0], matrix[:, 1], c=colors)
plt.title('Scatter-plot для матрицы 50x2')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# # 9. График функции z(x, y) = e^(x+y) * ln(xy)
# x = np.linspace(0.1, 2, 100)  # x > 0 для корректности ln(xy)
# y = np.linspace(0.1, 2, 100)
# X, Y = np.meshgrid(x, y)
# Z = np.exp(X + Y) * np.log(X * Y)  # Вычисление z
#
# plt.figure()
# plt.contourf(X, Y, Z, levels=20, cmap='viridis')  # Заливка цветом
# plt.colorbar()  # Шкала цветов
# # plt.title('$z(x, y) = e^{x + y} \cdot \ln(xy)$')
# plt.title(r'$z(x, y) = e^{x + y} \cdot \ln(xy)$')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Определяем функцию
def z_func(x, y):
    return np.exp(x + y) * np.log(x * y)

# Создаем сетку значений (x > 0, y > 0)
x = np.linspace(0.1, 2, 100)  # x > 0
y = np.linspace(0.1, 2, 100)  # y > 0
X, Y = np.meshgrid(x, y)
Z = z_func(X, Y)  # Вычисляем Z

# Настраиваем 3D-график
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Рисуем поверхность
surf = ax.plot_surface(
    X, Y, Z,
    cmap='viridis',      # Цветовая карта
    edgecolor='none',    # Убираем грани
    alpha=0.8,          # Прозрачность
    rstride=1,          # Шаг сетки по X
    cstride=1           # Шаг сетки по Y
)

# Добавляем цветовую шкалу
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Z')

# Настройка подписей
ax.set_title(r'$z(x, y) = e^{x + y} \cdot \ln(xy)$', fontsize=14)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)

# Убираем фоновые плоскости для лучшей видимости
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.tight_layout()
plt.show()