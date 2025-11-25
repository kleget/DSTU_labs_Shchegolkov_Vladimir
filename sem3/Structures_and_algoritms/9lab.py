class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        """Вставка элемента в дерево"""
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(self.root, value)
    
    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)
    
    def search(self, value):
        """Обычный поиск элемента"""
        return self._search(self.root, value)
    
    def _search(self, node, value):
        if node is None:
            return False
        
        if node.value == value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)
    
    def search_with_barrier(self, value):
        """Поиск с барьером"""
        # Создаем барьерный узел
        barrier = Node(value)
        
        def _search_barrier(node, target, barrier_node):
            if node is None:
                return False
                
            if node.value == target:
                return True
            elif target < node.value:
                if node.left is None:
                    node.left = barrier_node  # Устанавливаем барьер
                    return False
                return _search_barrier(node.left, target, barrier_node)
            else:
                if node.right is None:
                    node.right = barrier_node  # Устанавливаем барьер
                    return False
                return _search_barrier(node.right, target, barrier_node)
        
        result = _search_barrier(self.root, value, barrier)
        
        # Убираем барьер, если он был установлен
        self._remove_barrier(barrier)
        return result
    
    def _remove_barrier(self, barrier):
        """Удаление барьерного узла"""
        if self.root is None:
            return
            
        def _remove(node, barrier_node):
            if node is None:
                return node
                
            if node.left == barrier_node:
                node.left = None
                return node
            if node.right == barrier_node:
                node.right = None
                return node
                
            node.left = _remove(node.left, barrier_node)
            node.right = _remove(node.right, barrier_node)
            return node
        
        self.root = _remove(self.root, barrier)
    
    def delete(self, value):
        """Удаление элемента из дерева"""
        self.root = self._delete(self.root, value)
    
    def _delete(self, node, value):
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Узел с одним потомком или без потомков
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Узел с двумя потомками
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete(node.right, min_node.value)
        
        return node
    
    def _find_min(self, node):
        """Нахождение минимального элемента в поддереве"""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def print_tree(self):
        """Вывод дерева в виде структуры"""
        self._print_tree(self.root, 0)
    
    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.value)
            self._print_tree(node.left, level + 1)
    
    def inorder_traversal(self):
        """Центрированный обход (сортировка по возрастанию)"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

# Демонстрация работы
print("=== БИНАРНОЕ ДЕРЕВО ПОИСКА ===")

# Создаем дерево
bst = BinarySearchTree()
numbers = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

for num in numbers:
    bst.insert(num)

print("Структура дерева:")
bst.print_tree()

print("\nЦентрированный обход (отсортированный):")
print(bst.inorder_traversal())

# Поиск элементов
print("\n=== ПОИСК ЭЛЕМЕНТОВ ===")
test_values = [25, 55, 70, 100]

for val in test_values:
    found_normal = bst.search(val)
    found_barrier = bst.search_with_barrier(val)
    print(f"Значение {val}: обычный поиск = {found_normal}, с барьером = {found_barrier}")

# Удаление элемента
print("\n=== УДАЛЕНИЕ ЭЛЕМЕНТА 30 ===")
bst.delete(30)
print("Дерево после удаления:")
bst.print_tree()

print("\nЦентрированный обход после удаления:")
print(bst.inorder_traversal())