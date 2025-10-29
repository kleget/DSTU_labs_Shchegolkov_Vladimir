class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class StackLinked:
    """Стек на связном списке с сортировкой вставками"""
    
    def __init__(self):
        self.top = None
    
    def push(self, value):
        """Добавление элемента в стек"""
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        """Удаление и возврат верхнего элемента"""
        if self.top is None:
            return None
        value = self.top.value
        self.top = self.top.next
        return value
    
    def peek(self):
        """Просмотр верхнего элемента без удаления"""
        if self.top:
            return self.top.value
        return None
    
    def is_empty(self):
        """Проверка на пустоту"""
        return self.top is None
    
    def display(self):
        """Вывод содержимого стека"""
        current = self.top
        values = []
        while current:
            values.append(current.value)
            current = current.next
        print("Стек:", values)
    
    def insertion_sort(self):
        """Сортировка стека методом вставок"""
        if self.top is None or self.top.next is None:
            return  # Пустой стек или с одним элементом уже отсортирован
        
        # Создаем временный стек для отсортированных элементов
        sorted_stack = StackLinked()
        
        # Пока исходный стек не пуст
        while not self.is_empty():
            # Извлекаем текущий элемент из исходного стека
            current = self.pop()
            
            # Переносим элементы из отсортированного стека обратно в исходный,
            # пока не найдем правильную позицию для текущего элемента
            while not sorted_stack.is_empty() and sorted_stack.peek() > current:
                self.push(sorted_stack.pop())
            
            # Вставляем текущий элемент в отсортированный стек
            sorted_stack.push(current)
        
        # Переносим отсортированные элементы обратно в исходный стек
        while not sorted_stack.is_empty():
            self.push(sorted_stack.pop())

# Демонстрация работы
print("=== Сортировка стека методом вставок ===")

# Создаем стек с произвольными числами
stack = StackLinked()
stack.push(5)
stack.push(2)
stack.push(8)
stack.push(1)
stack.push(3)

print("Исходный стек:")
stack.display()

# Сортируем стек
stack.insertion_sort()

print("Отсортированный стек:")
stack.display()

# Еще один пример
print("\n=== Еще один пример ===")
stack2 = StackLinked()
for num in [9, 4, 6, 2, 7, 1]:
    stack2.push(num)

print("Исходный стек:")
stack2.display()

stack2.insertion_sort()
print("Отсортированный стек:")
stack2.display()
