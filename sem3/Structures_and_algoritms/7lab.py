class QueueArray:
    """Очередь на массиве"""
    
    def __init__(self, size=5):
        self.size = size
        self.queue = [None] * size
        self.front = 0
        self.rear = -1
        self.count = 0
    
    def enqueue(self, value):
        """Добавить элемент в конец"""
        if self.count == self.size:
            print("Очередь полна!")
            return
        
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = value
        self.count += 1
    
    def dequeue(self):
        """Удалить элемент из начала"""
        if self.count == 0:
            print("Очередь пуста!")
            return None
        
        value = self.queue[self.front]
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return value
    
    def display(self):
        """Показать очередь"""
        if self.count == 0:
            print("Очередь пуста")
            return
        
        print("Очередь:", end=" ")
        i = self.front
        for _ in range(self.count):
            print(self.queue[i], end=" ")
            i = (i + 1) % self.size
        print()

class QueueLinked:
    """Очередь на связном списке"""
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
    
    def __init__(self):
        self.front = None
        self.rear = None
    
    def enqueue(self, value):
        """Добавить элемент в конец"""
        new_node = self.Node(value)
        
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
    
    def dequeue(self):
        """Удалить элемент из начала"""
        if self.front is None:
            print("Очередь пуста!")
            return None
        
        value = self.front.value
        self.front = self.front.next
        
        if self.front is None:
            self.rear = None
            
        return value
    
    def display(self):
        """Показать очередь"""
        if self.front is None:
            print("Очередь пуста")
            return
        
        print("Очередь:", end=" ")
        current = self.front
        while current:
            print(current.value, end=" ")
            current = current.next
        print()

# Демонстрация работы
print("=== Очередь на массиве ===")
q1 = QueueArray(3)
q1.enqueue(1)
q1.enqueue(2)
q1.enqueue(3)
q1.display()
q1.enqueue(4)  # Переполнение
print("Удален:", q1.dequeue())
q1.display()

print("\n=== Очередь на списке ===")
q2 = QueueLinked()
q2.enqueue(10)
q2.enqueue(20)
q2.enqueue(30)
q2.display()
print("Удален:", q2.dequeue())
q2.display()