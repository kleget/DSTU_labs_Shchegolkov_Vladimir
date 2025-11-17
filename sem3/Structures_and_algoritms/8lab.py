class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def add_first(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def add_last(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def insert_after(self, after_value, new_value):
        current = self.head
        while current:
            if current.value == after_value:
                new_node = Node(new_value)
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next
        print("Элемент не найден")
    
    def delete(self, value):
        if not self.head:
            return
        
        if self.head.value == value:
            self.head = self.head.next
            return
        
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next
    
    def search(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1
    
    def display(self):
        if not self.head:
            print("Список пуст")
            return
        
        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")
    
    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

# Демонстрация
print("=== ЛИНЕЙНЫЙ СПИСОК ===")
lst = LinkedList()

# Добавляем элементы
lst.add_last(1)
lst.add_last(2)
lst.add_last(3)
lst.add_first(0)
print("Список после добавления:")
lst.display()

# Вставляем после элемента
lst.insert_after(1, 15)
print("После вставки 15 после 1:")
lst.display()

# Ищем элемент
print(f"Поиск 15: позиция {lst.search(15)}")
print(f"Поиск 99: позиция {lst.search(99)}")

# Удаляем элементы
lst.delete(0)
lst.delete(15)
print("После удаления 0 и 15:")
lst.display()

print(f"Длина списка: {lst.length()}")