class User:
    def __init__(self, name, order_id):
        self.name = name
        self.order_id = order_id
    
    def __str__(self):
        return f"{self.name} - заказ {self.order_id}"

class UserTree:
    def __init__(self):
        self.root = None
    
    def add(self, name, order_id):
        """Добавить пользователя"""
        new_user = User(name, order_id)
        
        if self.root is None:
            self.root = self.Node(new_user)
        else:
            self._add(self.root, new_user)
    
    class Node:
        def __init__(self, user):
            self.user = user
            self.left = None
            self.right = None
    
    def _add(self, node, new_user):
        if new_user.order_id < node.user.order_id:
            if node.left is None:
                node.left = self.Node(new_user)
            else:
                self._add(node.left, new_user)
        else:
            if node.right is None:
                node.right = self.Node(new_user)
            else:
                self._add(node.right, new_user)
    
    def find(self, order_id):
        """Найти пользователя по номеру заказа"""
        return self._find(self.root, order_id)
    
    def _find(self, node, order_id):
        if node is None:
            return None
        
        if node.user.order_id == order_id:
            return node.user
        elif order_id < node.user.order_id:
            return self._find(node.left, order_id)
        else:
            return self._find(node.right, order_id)
    
    def show_all(self):
        """Показать всех пользователей по порядку"""
        users = []
        self._get_sorted(self.root, users)
        return users
    
    def _get_sorted(self, node, users):
        if node:
            self._get_sorted(node.left, users)
            users.append(node.user)
            self._get_sorted(node.right, users)

# Простое использование
db = UserTree()

# Добавляем пользователей
db.add("Иван", 1003)
db.add("Мария", 1001) 
db.add("Алексей", 1005)
db.add("Ольга", 1002)
db.add("Дмитрий", 1004)

# Ищем заказы
print("Поиск заказов:")
print(f"Заказ 1001: {db.find(1001)}")
print(f"Заказ 1003: {db.find(1003)}")
print(f"Заказ 999: {db.find(999)}")

# Показываем всех
print("\nВсе пользователи (отсортировано):")
for user in db.show_all():
    print(f" - {user}")