# 1. В заданном тексте заменить слово А на слово В.
# 2. Для заданного текста определить длину содержащейся в нем максимальной
# серии символов, отличных от латинских букв.
#  6
# 3. Даны целые числа N (> 2), A и B. Сформировать и вывести целочисленный
# массив размера N, первый элемент которого равен A, второй равен B,
# а каждый последующий элемент равен сумме всех предыдущих
# 4. Найти произведение элементов массива, значения которых нечетные числа.

#1 В заданном тексте заменить слово А на слово В.
text = input("Введите текст: ")
A = input("Введите слово которое надо заменить: ")
B = input("Введите слово на которое будем заменять: ")
print(text.replace(A, B))
#2 Для заданного текста определить длину содержащейся в нем максимальной
# серии символов, отличных от латинских букв.
a = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Z", "A", "E", "I", "O", "U"]
a = set(a)
TEXT = text.upper()
m = 0
o = 0
for i in range(len(TEXT)):
    if TEXT[i] not in a:
        o += 1
    else:
        m = o
        o = 0
print(m)

#3
N = int(input('Введите N: '))
A = int(input('Введите A: '))
B = int(input('Введите B: '))
if N <= 2:
    print('Условия читай')
    exit()
else:
    m = [A, B]
    for x in range(N):
        m.append(sum(m))
    print(m)

#4
m = input('Введите массив чисел через пробел: ').split(' ')
answ_4 = 1
for x in range(len(m)):
    if int(m[x])%2==1:
        answ_4 *= int(m[x])
print(answ_4)
