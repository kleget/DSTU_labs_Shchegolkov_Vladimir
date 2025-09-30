import os
import random

def create_real_numbers_file(filename):
    """Создание файла действительных чисел"""
    with open(filename, 'w') as f:
        # Генерируем 20 случайных чисел (положительных и отрицательных)
        for _ in range(20):
            num = random.uniform(-100, 100)
            f.write(f"{num}\n")

def count_negative_numbers(filename):
    """Подсчет количества отрицательных чисел в файле"""
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            num = float(line.strip())
            if num < 0:
                count += 1
    return count

def add_char_to_file(filename, char, position):
    """Добавление символа в произвольное место файла"""
    # Читаем содержимое файла
    with open(filename, 'r') as f:
        content = f.read()
    
    # Вставляем символ в указанную позицию
    new_content = content[:position] + char + content[position:]
    
    # Записываем обратно в файл
    with open(filename, 'w') as f:
        f.write(new_content)

def create_text_file(filename):
    """Создание текстового файла с произвольным текстом"""
    sample_text = """Первая строка текста.
Вторая строка с некоторым содержанием.
Третья строка файла.
Четвертая и последняя строка."""
    
    with open(filename, 'w') as f:
        f.write(sample_text)

def get_nth_line(filename, n):
    """Получение n-й строки из файла"""
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f, 1):
                if i == n:
                    return line.strip()
        return f"Строка с номером {n} не найдена"
    except:
        return "Ошибка при чтении файла"

def find_substring_in_file(filename, substring):
    """Поиск подстроки в файле"""
    results = []
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            pos = line.find(substring)
            while pos != -1:
                results.append((line_num, pos + 1))  # +1 так как позиции начинаются с 1
                pos = line.find(substring, pos + 1)
    return results

def count_unique_words(filename):
    """Подсчет уникальных слов в файле"""
    words = set()
    with open(filename, 'r') as f:
        for line in f:
            # Разбиваем строку на слова, игнорируя регистр
            line_words = line.lower().split()
            for word in line_words:
                # Убираем знаки препинания вокруг слов
                word = word.strip('.,!?;:"()')
                if word:
                    words.add(word)
    return len(words)

def count_word_occurrences(filename):
    """Подсчет количества вхождений каждого слова"""
    word_count = {}
    with open(filename, 'r') as f:
        for line in f:
            # Разбиваем строку на слова, игнорируя регистр
            line_words = line.lower().split()
            for word in line_words:
                # Убираем знаки препинания вокруг слов
                word = word.strip('.,!?;:"()')
                if word:
                    word_count[word] = word_count.get(word, 0) + 1
    return word_count

def main():
    # Задание 1
    print("Задание 1: Создание файла действительных чисел и подсчет отрицательных чисел")
    real_file = "real_numbers.txt"
    create_real_numbers_file(real_file)
    negative_count = count_negative_numbers(real_file)
    print(f"Количество отрицательных чисел в файле: {negative_count}")
    print()
    
    # Задание 2
    print("Задание 2: Добавление символа в файл")
    char_file = "char_file.txt"
    with open(char_file, 'w') as f:
        f.write("Это тестовый текст для демонстрации.")
    
    print("Содержимое файла до добавления символа:")
    with open(char_file, 'r') as f:
        print(f.read())
    
    add_char_to_file(char_file, "X", 10)
    
    print("Содержимое файла после добавления символа 'X' на позицию 10:")
    with open(char_file, 'r') as f:
        print(f.read())
    print()
    
    # Задание 3
    print("Задание 3: Работа с текстовым файлом")
    text_file = "text_file.txt"
    create_text_file(text_file)
    
    n = 2
    print(f"Содержимое {n}-й строки: {get_nth_line(text_file, n)}")
    print()
    
    # Задание 4
    print("Задание 4: Поиск подстроки в файле")
    substring = "строка"
    results = find_substring_in_file(text_file, substring)
    print(f"Подстрока '{substring}' найдена в позициях:")
    for line_num, pos in results:
        print(f"  Строка {line_num}, позиция {pos}")
    print()
    
    # Задание 5
    print("Задание 5: Статистика по словам в файле")
    unique_words = count_unique_words(text_file)
    print(f"Количество уникальных слов: {unique_words}")
    
    word_stats = count_word_occurrences(text_file)
    print("Количество вхождений каждого слова:")
    for word, count in word_stats.items():
        print(f"  {word}: {count}")

if __name__ == "__main__":
    main()

файл тхт с должниками есть имя и долг
коллектор запускает прогу, если сумма долга больше 10к то гг