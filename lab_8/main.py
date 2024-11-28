#1
hours = int(input('Часы: '))
minutes = int(input('Минуты: '))
seconds = int(input('Секунды: '))
T = int(input('На сколько увеличить время: '))

def IncTime(H, M, S, T):
    S += T
    while S > 60:
        S-=60
        M+=1
    while M > 60:
        M-=60
        H+=1
    return (H, M, S)



a = IncTime(hours, minutes, seconds, T)
print(f'Hours: {a[0]}, M0nutes: {a[1]}, Seconds: {a[2]}')

#2
from pprint import pprint
A = (5, 10)
a = input('Введите матрицу в формате: 1,2,3, 4,5,6, 7,8,9')
a = a.split(', ')
for x in range(len(a)):
    a[x] = a[x].split(',')

#проверка на квадратность
def proverka(a):
    flag = True
    for x in range(len(a)):
        if len(a) != len(a[x]):
            return False
    if flag == True:
        return True

def main(a):
    if proverka(a):
        R = len(a) * [len(a) * [0]]
        R = [list(sublist) for sublist in R]
        #тут отображаем нижнетреугольную матрицу
        for i in range(len(a)):
            for j in range(len(a)):
                if j <= i:
                    R[i][j] = a[i][j]
        #тут добавляем элементы побочной диагонали
        i = len(a) - 1
        j = 0
        while j <= len(a)-1 and i >=0:
            R[i][j] = a[i][j]
            i-=1
            j+=1

        return R

w = main(a)
for e in range(len(w)):
    print(w[e])


#3
def is_power_of_two(n):
    if n == 1:
        return "YES"
    if n % 2 != 0 or n == 0:
        return "NO"
    return is_power_of_two(n // 2)

N = int(input("Введите натуральное число N: "))
print(is_power_of_two(N))



# print(proverka(a))