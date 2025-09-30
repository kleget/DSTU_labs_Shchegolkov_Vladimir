def input_set():
    """Функция для ввода элементов множества с клавиатуры."""
    user_input = input("Введите элементы множества через запятую (можно использовать диапазоны через ..): ")
    elements = []
    for part in user_input.split(','):
        part = part.strip()
        if '..' in part:
            start, end = part.split('..')
            start = start.strip()
            end = end.strip()
            if start.isdigit() and end.isdigit():
                elements.extend(range(int(start), int(end) + 1))
            else:
                elements.extend([chr(i) for i in range(ord(start), ord(end) + 1)])
        else:
            if part.isdigit():
                elements.append(int(part))
            else:
                elements.append(part)
    return set(elements)

def printset(s, name="Множество"):
    """Функция для печати элементов множества и их количества."""
    print(f"{name} содержит {len(s)} элементов: {s}")

# Задание 1 и 2
print("Задание 1 и 2")
set_A = input_set()
printset(set_A, "Множество A")

set_B = input_set()
printset(set_B, "Множество B")

# Задание 3
def common_words(s1, s2):
    """Нахождение общих слов без использования операций над множествами."""
    common = set()
    for word in s1:
        if word in s2:
            common.add(word)
    return common

print("\nЗадание 3")
sentence1 = input("Введите первое предложение: ").lower().split()
sentence2 = input("Введите второе предложение: ").lower().split()

set1 = set(sentence1)
set2 = set(sentence2)

common = common_words(set1, set2)
print("Общие слова:", common)

# Задание 4
def classify_chars(s):
    """Разделение символов на русские, латинские и цифры."""
    rus = set()
    lat = set()
    digits = set()
    
    for char in s:
        if 'а' <= char <= 'я' or 'А' <= char <= 'Я':
            rus.add(char)
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            lat.add(char)
        elif char.isdigit():
            digits.add(char)
    return rus, lat, digits

print("\nЗадание 4")
input_chars = input("Введите строку символов: ")
set_S = set(input_chars)

rus_set, lat_set, digit_set = classify_chars(set_S)

printset(rus_set, "Русские символы")
printset(lat_set, "Латинские символы")
printset(digit_set, "Цифры")