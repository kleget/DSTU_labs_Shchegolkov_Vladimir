class MemoryManager:
    def __init__(self):
        self.segments = [[None] * 32 for _ in range(4)]
        self.pointers = {}
    
    def get_free_space(self):
        return [sum(1 for cell in seg if cell is None) for seg in self.segments]
    
    def find_best_segment(self, size):
        free_spaces = self.get_free_space()
        best_seg = None
        best_offset = None
        max_diff = -1
        
        for seg_num in range(4):
            for offset in range(33 - size):
                if all(self.segments[seg_num][offset + i] is None for i in range(size)):
                    # Вычисляем новое распределение памяти
                    new_free = free_spaces.copy()
                    new_free[seg_num] -= size
                    
                    # Находим максимальную разницу
                    diff = max(new_free) - min(new_free)
                    
                    if diff > max_diff:
                        max_diff = diff
                        best_seg = seg_num
                        best_offset = offset
        
        return best_seg, best_offset
    
    def create_pointer(self, name, data_type):
        sizes = {'byte': 1, 'int': 2, 'longint': 4}
        size = sizes[data_type]
        
        seg, offset = self.find_best_segment(size)
        if seg is None:
            return "Недостаточно памяти"
        
        # Занимаем память
        for i in range(size):
            self.segments[seg][offset + i] = name
        
        self.pointers[name] = {
            'segment': seg,
            'offset': offset,
            'size': size,
            'type': data_type,
            'value': None
        }
        
        free = self.get_free_space()
        print(f"Создан {name} в сегменте {seg}. Свободно: {free}")
    
    def write_pointer(self, name, value):
        if name in self.pointers:
            self.pointers[name]['value'] = value
            print(f"Записано {value} в {name}")
    
    def read_pointer(self, name):
        if name in self.pointers:
            return self.pointers[name]['value']
        return "Указатель не найден"
    
    def free_pointer(self, name):
        if name in self.pointers:
            info = self.pointers[name]
            seg, offset, size = info['segment'], info['offset'], info['size']
            
            # Освобождаем память
            for i in range(size):
                self.segments[seg][offset + i] = None
            
            del self.pointers[name]
            free = self.get_free_space()
            print(f"Освобожден {name}. Свободно: {free}")

# Демонстрация
mm = MemoryManager()

# Создаем указатели
mm.create_pointer('p1', 'byte')
mm.create_pointer('p2', 'int') 
mm.create_pointer('p3', 'longint')
mm.create_pointer('p4', 'byte')

# Работаем с указателями
mm.write_pointer('p1', 10)
mm.write_pointer('p2', 1000)
print(f"p1 = {mm.read_pointer('p1')}")

# Освобождаем память
mm.free_pointer('p2')