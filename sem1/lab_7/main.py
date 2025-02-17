#1
dictionary_1 = {'a':300,
              'b':400}
dictionary_2 = {'c': 500,
                'd':600}

dict_answ = dictionary_1 | dictionary_2
print(dict_answ)

#2
Capitals = {
"Россия": "Москва",
"Канада": "Оттава",
"Китай": "Пекин",
"Соединённые Штаты Америки (США)": "Вашингтон",
"Бразилия":"Бразилиа"}

a = input('Введите предложение: ')
for x in Capitals:
    if x in a:
        print(Capitals[x])

#3
from random import randint
M = int(input('Введите порядок матрицы: '))
A = M*[M*[0]]
A = [list(sublist) for sublist in A]
for x in range(len(A)):
    for y in range(len(A)):
        A[x][y] = randint(1, 100)

answ = 0
for x in range(len(A)):
    for y in range(len(A[x])):
        answ += A[x][y]
print(answ)
