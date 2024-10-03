# задание #5

# |R = это действительные числа(float)
import math

x = float(input('Введите x:'))
y = float(input('Введите y:'))
z = float(input('Введите z:'))

if x>y>z:
    x *= 2
    y *= 2
    z *= 2
else:
    x = math.fabs(x)
    y = math.fabs(y)
    z = math.fabs(z)

