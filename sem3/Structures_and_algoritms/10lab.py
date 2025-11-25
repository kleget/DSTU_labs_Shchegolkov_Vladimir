class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def hash_function(self, key):
        """Простая хеш-функция - сумма кодов букв"""
        return sum(ord(char) for char in key) % self.size
    
    def insert(self, key):
        """Вставка ключа в хеш-таблицу"""
        index = self.hash_function(key)
        self.table[index].append(key)
    
    def search(self, key):
        """Поиск ключа с подсчетом шагов"""
        index = self.hash_function(key)
        chain = self.table[index]
        
        steps = 0
        for item in chain:
            steps += 1
            if item == key:
                return True, steps
        return False, steps
    
    def display(self):
        """Вывод хеш-таблицы"""
        for i in range(self.size):
            print(f"{i}: {self.table[i]}")
    
    def statistics(self):
        """Статистика по таблице"""
        total_items = 0
        max_chain = 0
        empty_cells = 0
        
        for chain in self.table:
            total_items += len(chain)
            max_chain = max(max_chain, len(chain))
            if len(chain) == 0:
                empty_cells += 1
        
        print(f"Всего элементов: {total_items}")
        print(f"Размер таблицы: {self.size}")
        print(f"Максимальная длина цепочки: {max_chain}")
        print(f"Пустых ячеек: {empty_cells}")
        print(f"Коэффициент заполнения: {total_items/self.size:.2f}")

# Демонстрация работы
print("=== ХЕШ-ТАБЛИЦА С МЕТОДОМ ЦЕПОЧЕК ===")

# Создаем хеш-таблицу
ht = HashTable(10)

# Тестовые данные - животные
animals = ["лев", "тигр", "медведь", "волк", "лиса", "заяц", 
          "слон", "жираф", "зебра", "носорог", "бегемот", "крокодил"]

# Вставляем элементы
for animal in animals:
    ht.insert(animal)

# Показываем таблицу
print("\nХеш-таблица:")
ht.display()

# Статистика
print("\nСтатистика:")
ht.statistics()

# Поиск элементов
print("\nПоиск элементов:")
test_items = ["лев", "тигр", "пантера", "слон", "обезьяна"]

for item in test_items:
    found, steps = ht.search(item)
    status = "найден" if found else "не найден"
    print(f"'{item}': {status} за {steps} шагов")

# Сравнение с другой хеш-функцией
print("\n" + "="*50)
print("СРАВНЕНИЕ С ДРУГОЙ ХЕШ-ФУНКЦИЕЙ")

class HashTable2(HashTable):
    def hash_function(self, key):
        """Альтернативная хеш-функция - произведение кодов"""
        product = 1
        for char in key:
            product = (product * ord(char)) % self.size
        return product

ht2 = HashTable2(10)
for animal in animals:
    ht2.insert(animal)

print("\nХеш-таблица с альтернативной функцией:")
ht2.display()
print("\nСтатистика:")
ht2.statistics()