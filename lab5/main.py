# вариант 15
#1
answ_1 = 1
for i in range(1, 50+1):
    if i %2 ==0:
        answ_1 *= i*2
print(answ_1)

#2
n = int(input('Введите n: '))
answ_2 = 0
for k in range(1, n+1):
    answ_2 += ((-1**k)/((2*k+1)*k))

print(answ_2)
#3

from math import e

x = -5
h = 0.1
answ_3 = []
while x <=5:
    answ_3.append(e**x/((x+2)**2))
    x += h

print(answ_3)