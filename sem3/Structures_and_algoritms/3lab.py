class MemoryManager:
    """Менеджер памяти для эмуляции работы с указателями"""
    
    def __init__(self):
        # Статический сегмент: информация об указателях
        self.static_segment = {}  # {имя: {'segment', 'offset', 'size', 'value'}}
        
        # 4 сегмента динамической памяти по 32 байта каждый
        self.dynamic_segments = [
            [None] * 32,  # Сегмент 0
            [None] * 32,  # Сегмент 1  
            [None] * 32,  # Сегмент 2
            [None] * 32   # Сегмент 3
        ]
        
        # Размеры типов данных в байтах
        self.type_sizes = {
            'byte': 1,
            'int': 2,
            'longint': 4
        }

    def find_free_space(self, size):
        """Поиск свободного места в динамических сегментах"""
        for seg_num in range(4):
            for i in range(0, 32 - size + 1):
                # Проверяем, свободен ли блок нужного размера
                if all(self.dynamic_segments[seg_num][i + j] is None 
                       for j in range(size)):
                    return seg_num, i
        return None, None  # Нет свободного места

    def NewPointer(self, name, data_type):
        """Создание нового указателя"""
        if name in self.static_segment:
            print(f"Указатель '{name}' уже существует. Эмуляция утечки памяти.")
            # Эмуляция утечки: старую память не освобождаем, выделяем новую
        
        if data_type not in self.type_sizes:
            raise ValueError(f"Неизвестный тип данных: {data_type}")
        
        size = self.type_sizes[data_type]
        seg_num, offset = self.find_free_space(size)
        
        if seg_num is None:
            raise MemoryError("Недостаточно свободной памяти для выделения")
        
        # Резервируем память
        for i in range(size):
            self.dynamic_segments[seg_num][offset + i] = name
        
        # Сохраняем информацию в статическом сегменте
        self.static_segment[name] = {
            'segment': seg_num,
            'offset': offset,
            'size': size,
            'type': data_type,
            'value': None  # Изначально значение не установлено
        }
        
        print(f"Создан указатель '{name}' типа {data_type} в сегменте {seg_num}, смещение {offset}")

    def WritePointer(self, name, value):
        """Запись значения в указатель"""
        if name not in self.static_segment:
            raise KeyError(f"Указатель '{name}' не найден")
        
        info = self.static_segment[name]
        
        # Проверяем диапазон значений в зависимости от типа
        if info['type'] == 'byte':
            if not (0 <= value <= 255):
                raise ValueError("Byte должен быть в диапазоне 0-255")
        elif info['type'] == 'int':
            if not (-32768 <= value <= 32767):
                raise ValueError("Int должен быть в диапазоне -32768..32767")
        elif info['type'] == 'longint':
            if not (-2147483648 <= value <= 2147483647):
                raise ValueError("Longint должен быть в диапазоне -2147483648..2147483647")
        
        # Записываем значение
        info['value'] = value
        print(f"Записано значение {value} в указатель '{name}'")

    def ReadPointer(self, name):
        """Чтение значения указателя"""
        if name not in self.static_segment:
            raise KeyError(f"Указатель '{name}' не найден")
        
        info = self.static_segment[name]
        
        if info['value'] is None:
            print(f"Предупреждение: указатель '{name}' не инициализирован")
            return None
        
        return info['value']

    def SetPointer(self, name1, name2):
        """Присвоение значения одного указателя другому"""
        if name1 not in self.static_segment:
            raise KeyError(f"Указатель '{name1}' не найден")
        if name2 not in self.static_segment:
            raise KeyError(f"Указатель '{name2}' не найден")
        
        value = self.ReadPointer(name2)
        if value is not None:
            self.WritePointer(name1, value)
            print(f"Значение указателя '{name2}' скопировано в '{name1}'")

    def FreePointer(self, name):
        """Освобождение памяти, занимаемой указателем"""
        if name not in self.static_segment:
            raise KeyError(f"Указатель '{name}' не найден")
        
        info = self.static_segment[name]
        seg_num = info['segment']
        offset = info['offset']
        size = info['size']
        
        # Освобождаем память в динамическом сегменте
        for i in range(size):
            self.dynamic_segments[seg_num][offset + i] = None
        
        # Удаляем информацию из статического сегмента
        del self.static_segment[name]
        print(f"Память указателя '{name}' освобождена")

    def display_memory(self):
        """Отображение состояния памяти"""
        print("\n=== СОСТОЯНИЕ ПАМЯТИ ===")
        print("Статический сегмент (информация об указателях):")
        for name, info in self.static_segment.items():
            print(f"  {name}: сегмент={info['segment']}, смещение={info['offset']}, "
                  f"тип={info['type']}, значение={info['value']}")
        
        print("\nДинамические сегменты:")
        for i, segment in enumerate(self.dynamic_segments):
            occupied = sum(1 for cell in segment if cell is not None)
            print(f"  Сегмент {i}: занято {occupied}/32 байт")
            # Детализация занятых ячеек
            for j in range(0, 32, 8):
                line = segment[j:j+8]
                display_line = [f"{cell[:3]}..." if cell else "FREE" for cell in line]
                print(f"    {j:2d}-{j+7:2d}: {display_line}")

def main():
    """Демонстрация работы менеджера памяти"""
    mm = MemoryManager()
    
    try:
        # Создание указателей
        print("=== СОЗДАНИЕ УКАЗАТЕЛЕЙ ===")
        mm.NewPointer('p1', 'byte')
        mm.NewPointer('p2', 'int')
        mm.NewPointer('p3', 'longint')
        
        # Запись значений
        print("\n=== ЗАПИСЬ ЗНАЧЕНИЙ ===")
        mm.WritePointer('p1', 42)
        mm.WritePointer('p2', 1000)
        mm.WritePointer('p3', 1000000)
        
        # Чтение значений
        print("\n=== ЧТЕНИЕ ЗНАЧЕНИЙ ===")
        print(f"p1 = {mm.ReadPointer('p1')}")
        print(f"p2 = {mm.ReadPointer('p2')}")
        print(f"p3 = {mm.ReadPointer('p3')}")
        
        # Копирование значений между указателями
        print("\n=== КОПИРОВАНИЕ ЗНАЧЕНИЙ ===")
        mm.NewPointer('p4', 'int')
        mm.SetPointer('p4', 'p2')  # Копируем p2 в p4
        
        # Эмуляция утечки памяти
        print("\n=== ЭМУЛЯЦИЯ УТЕЧКИ ПАМЯТИ ===")
        mm.NewPointer('p1', 'byte')  # Пересоздаем p1 (утечка)
        mm.WritePointer('p1', 123)
        
        # Попытка чтения неинициализированного указателя
        print("\n=== ЧТЕНИЕ НЕИНИЦИАЛИЗИРОВАННОГО УКАЗАТЕЛЯ ===")
        mm.NewPointer('p5', 'byte')
        mm.ReadPointer('p5')
        
        # Отображение состояния памяти
        mm.display_memory()
        
        # Освобождение памяти
        print("\n=== ОСВОБОЖДЕНИЕ ПАМЯТИ ===")
        mm.FreePointer('p2')
        mm.FreePointer('p3')
        mm.FreePointer('p4')
        
        # Финальное состояние памяти
        mm.display_memory()
        
        # Обработка ошибок
        print("\n=== ОБРАБОТКА ОШИБОК ===")
        try:
            mm.ReadPointer('nonexistent')
        except KeyError as e:
            print(f"Ошибка: {e}")
        
        try:
            mm.WritePointer('p1', 300)  # Неверное значение для byte
        except ValueError as e:
            print(f"Ошибка: {e}")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()