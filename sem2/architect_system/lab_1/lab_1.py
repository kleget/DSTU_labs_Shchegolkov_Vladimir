import xml.etree.ElementTree as ET
import os

FILENAME = "shovels.xml"


def create_xml():
    if not os.path.exists(FILENAME):
        root = ET.Element("shovels")
        tree = ET.ElementTree(root)
        tree.write(FILENAME)


def add_shovel(article, shovel_type, color, responsible=None):
    tree = ET.parse(FILENAME)
    root = tree.getroot()

    shovel = ET.Element("shovel")
    shovel.set("article", article)

    type_elem = ET.SubElement(shovel, "type")
    type_elem.text = shovel_type

    color_elem = ET.SubElement(shovel, "color")
    color_elem.text = color

    responsible_elem = ET.SubElement(shovel, "responsible")
    responsible_elem.text = responsible if responsible else "None"

    root.append(shovel)
    tree.write(FILENAME)
    print("Лопата добавлена.")


def list_shovels():
    tree = ET.parse(FILENAME)
    root = tree.getroot()

    if not root:
        print("Список лопат пуст.")
        return

    with_responsible = []
    without_responsible = []

    for shovel in root.findall("shovel"):
        article = shovel.get("article")
        shovel_type = shovel.find("type").text
        color = shovel.find("color").text
        responsible = shovel.find("responsible").text if shovel.find("responsible") is not None else "None"

        if responsible == "None":
            without_responsible.append(
                f"Артикул: {article}, Тип: {shovel_type}, Цвет: {color}, Ответственный: {responsible}")
        else:
            with_responsible.append(
                f"Артикул: {article}, Тип: {shovel_type}, Цвет: {color}, Ответственный: {responsible}")

    print("\nЛопаты с ответственными:")
    if with_responsible:
        for item in with_responsible:
            print(item)
    else:
        print("Нет лопат с ответственными.")

    print("\nЛопаты без ответственных:")
    if without_responsible:
        for item in without_responsible:
            print(item)
    else:
        print("Все лопаты имеют ответственного.")


def remove_shovel(article):
    tree = ET.parse(FILENAME)
    root = tree.getroot()

    for shovel in root.findall("shovel"):
        if shovel.get("article") == article:
            root.remove(shovel)
            tree.write(FILENAME)
            print("Лопата удалена.")
            return
    print("Лопата с таким артикулом не найдена.")


def main():
    create_xml()
    while True:
        print("\n1. Вывести список лопат")
        print("2. Добавить лопату")
        print("3. Удалить лопату")
        print("4. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            list_shovels()
        elif choice == "2":
            article = input("Введите артикул: ")
            shovel_type = input("Введите тип: ")
            color = input("Введите цвет: ")
            responsible = input("Введите ответственного (если нет, оставить пустым): ") or None
            add_shovel(article, shovel_type, color, responsible)
        elif choice == "3":
            article = input("Введите артикул для удаления: ")
            remove_shovel(article)
        elif choice == "4":
            break
        else:
            print("Некорректный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
