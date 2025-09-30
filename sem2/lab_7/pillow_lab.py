from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import random


# ---------------------- Задание 1 ----------------------
def task1():
    img = Image.open("shrek.jpeg")
    # 1. Обрезать изображение (пример: центральная часть)
    width, height = img.size
    cropped = img.crop((width // 4, height // 4, 3 * width // 4, 3 * height // 4))

    # 2. Добавить текст и графику
    draw = ImageDraw.Draw(cropped)
    # Текст
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((10, 10), "ЭТО ШРЭК!", font=font, fill="red")
    # Графика (прямоугольник)
    draw.rectangle([100, 100, 200, 200], outline="blue", width=5)

    # 3. Размыть часть изображения
    blurred_region = cropped.crop((100, 50, 1000, 630)).filter(ImageFilter.GaussianBlur(20))
    cropped.paste(blurred_region, (50, 50))

    # 4. Сохранить
    cropped.save("task1_result.jpg")


# ---------------------- Задание 2 ----------------------
def task2():
    img = Image.open("shrek.jpeg")
    # 2. Вырезать фрагмент
    width, height = img.size
    fragment = img.crop((width // 3, height // 4, 3 * width // 4.5, 3 * height // 4))
    # 3. Обрезать с помощью срезов (уже сделано)
    # 4. Увеличить размер
    resized = fragment.resize((fragment.width * 2, fragment.height * 2))
    resized.save("task2_resized.jpg")
    # 5. Повернуть на 45 градусов
    rotated = resized.rotate(45, expand=True)
    rotated.save("task2_rotated.jpg")
    # 6. Чёрно-белое
    bw = resized.convert("L")
    bw.save("task2_bw.jpg")


# ---------------------- Задание 3 ----------------------
def task3():
    img = Image.open("shrek.jpeg")
    # 2. Поменять левую и правую половины
    width, height = img.size
    left = img.crop((0, 0, width // 2, height))
    right = img.crop((width // 2, 0, width, height))
    swapped = Image.new("RGB", (width, height))
    swapped.paste(right, (0, 0))
    swapped.paste(left, (width // 2, 0))
    # 3. Добавить текст
    draw = ImageDraw.Draw(swapped)
    font = ImageFont.truetype("arial.ttf", 60)
    draw.text((width // 2 - 150, 50), "Mirror", fill="yellow", font=font)
    swapped.save("task3_result.jpg")


# ---------------------- Задание 4 ----------------------
def task4():
    # 1. Используем два изображения (shrek.jpg и другое, например, shrek2.jpg)
    img1 = Image.open("shrek.jpeg")
    img2 = Image.open("me.JPG")  # Для примера, замените на второе изображение
    # 2. Применить фильтр
    filtered = img1.filter(ImageFilter.SHARPEN)
    filtered.save("task4_filtered.jpg")
    # 3. Закрасить область и вставить второе изображение
    draw = ImageDraw.Draw(img2)
    draw.rectangle([500, 500, 1500, 1500], fill="black")
    img2.paste(filtered.resize((1000, 1000)), (500, 500))
    img2.save("task4_combined.jpg")


# ---------------------- Задание 5 ----------------------
def task5():
    img = Image.open("shrek.jpeg")
    # 2. Пример: умножение пикселей на 1.5
    arr = np.array(img)
    arr = np.clip(arr * 1.5, 0, 255).astype('uint8')
    result = Image.fromarray(arr)
    result.save("task5_result.jpg")


# ---------------------- Задание 6 ----------------------
def task6():
    # 1. Используем несколько изображений (shrek.jpg и другие)
    images = [Image.open("shrek.jpeg"), Image.open("sky.JPG")]  # Замените на другие
    # 2. Создать коллаж (2 изображения рядом)
    collage = Image.new("RGB", (images[0].width * 2, images[0].height))
    collage.paste(images[0], (0, 0))
    collage.paste(images[1], (images[0].width, 0))
    collage.save("task6_collage.png")


# ---------------------- Задание 7 ----------------------
def task7():
    # 1. Создать словарь
    image_dict = {
        "Шрек": Image.open("shrek.jpeg"),
        "Хеллоу Китти": Image.open("hello_kitty.jpg")  # Добавьте другие изображения
    }

    score = 0
    keys = list(image_dict.keys())
    random.shuffle(keys)

    for key in keys:
        image = image_dict[key]
        image.show()
        user_input = input("Что изображено на картинке? ")
        if user_input.strip().lower() == key.lower():
            print("Правильно!")
            score += 1
        else:
            print(f"Неправильно. Правильный ответ: {key}")

    print(f"Правильных ответов: {score}/{len(keys)}")


# Выполнение заданий
task1()
task2()
task3()
task4()  # Требует второе изображение
task5()
task6()  # Требует дополнительные изображения
task7()  # Требует дополнительные изображения