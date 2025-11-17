class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def add_sorted(self, value):
        """Добавляем элемент в отсортированный список"""
        new_node = Node(value)
        
        if not self.head or value < self.head.value:
            new_node.next = self.head
            self.head = new_node
            return
        
        current = self.head
        while current.next and current.next.value < value:
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
    
    def get_node(self, index):
        """Получаем узел по индексу (медленно!)"""
        current = self.head
        for i in range(index):
            if not current:
                return None
            current = current.next
        return current
    
    def length(self):
        """Считаем длину списка"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def binary_search(self, target):
        """Бинарный поиск в связном списке"""
        left, right = 0, self.length() - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_node = self.get_node(mid)
            
            if not mid_node:
                return -1
            
            if mid_node.value == target:
                return mid
            elif mid_node.value < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    def display(self):
        """Показываем список"""
        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

# Демонстрация
lst = LinkedList()

# Создаем отсортированный список
for num in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]:
    lst.add_sorted(num)

print("Список:")
lst.display()

# Ищем элементы
print(f"\nПоиск 16: индекс {lst.binary_search(16)}")
print(f"Поиск 38: индекс {lst.binary_search(38)}") 
print(f"Поиск 100: индекс {lst.binary_search(100)}")