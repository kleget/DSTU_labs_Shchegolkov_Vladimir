class StackArray:
    """Стек на массиве"""
    
    def __init__(self):
        self.stack = []
    
    def push(self, value):
        """Добавить элемент"""
        self.stack.append(value)
    
    def pop(self):
        """Удалить элемент"""
        if self.stack:
            return self.stack.pop()
        return None
    
    def peek(self):
        """Посмотреть верхний элемент"""
        if self.stack:
            return self.stack[-1]
        return None
    
    def is_empty(self):
        """Проверить пустоту"""
        return len(self.stack) == 0
    
    def display(self):
        """Показать стек"""
        print("Стек:", self.stack)

class StackLinked:
    """Стек на связном списке"""
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
    
    def __init__(self):
        self.top = None
    
    def push(self, value):
        """Добавить элемент"""
        new_node = self.Node(value)
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        """Удалить элемент"""
        if self.top is None:
            return None
        value = self.top.value
        self.top = self.top.next
        return value
    
    def peek(self):
        """Посмотреть верхний элемент"""
        if self.top:
            return self.top.value
        return None
    
    def is_empty(self):
        """Проверить пустоту"""
        return self.top is None
    
    def display(self):
        """Показать стек"""
        current = self.top
        values = []
        while current:
            values.append(current.value)
            current = current.next
        print("Стек:", values)

# Простое тестирование
print("=== Стек на массиве ===")
s1 = StackArray()
s1.push(1)
s1.push(2)
s1.push(3)
s1.display()
print("Верхний:", s1.peek())
print("Удален:", s1.pop())
s1.display()

print("\n=== Стек на списке ===")
s2 = StackLinked()
s2.push(10)
s2.push(20)
s2.push(30)
s2.display()
print("Верхний:", s2.peek())
print("Удален:", s2.pop())
s2.display()
