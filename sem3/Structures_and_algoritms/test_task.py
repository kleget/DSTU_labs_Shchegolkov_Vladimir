class Node:
    """Узел односвязного списка"""
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    """Односвязный список с поиском с барьером"""
    
    def __init__(self):
        self.head = None
    
    def add(self, value):
        """Добавление элемента в конец списка"""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
    
    def search_with_barrier(self, target):
        """Поиск с барьером"""
        if self.head is None:
            return None
        
        # Создаем барьерный узел с искомым значением
        barrier = Node(target)
        
        # Находим последний узел и прикрепляем к нему барьер
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = barrier
        
        # Теперь ищем целевой элемент
        current = self.head
        while current.value != target:
            current = current.next
        
        # Удаляем барьер
        current = self.head
        while current.next != barrier:
            current = current.next
        current.next = None
        
        # Проверяем, нашли ли мы целевой элемент или барьер
        if current.value == target:
            return current
        return None
    
    def print_list(self):
        """Печать списка"""
        current = self.head
        while current is not None:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

# Демонстрация работы
lst = LinkedList()
lst.add(5)
lst.add(2)
lst.add(8)
lst.add(1)
lst.add(9)

print("Исходный список:")
lst.print_list()

# Поиск существующего элемента
result = lst.search_with_barrier(8)
print(f"\nНайден элемент: {result.value if result else 'Не найден'}")

# Поиск несуществующего элемента
result = lst.search_with_barrier(15)
print(f"Найден элемент: {result.value if result else 'Не найден'}")

print("\nСписок после поиска (не изменился):")
lst.print_list()