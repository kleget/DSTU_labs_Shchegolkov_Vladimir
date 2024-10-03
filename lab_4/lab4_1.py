#задание #16

import math

x = int(input('Введите значение для расчетов:'))

answer_by_formula = (math.tan(x)/x) + math.pow(math.sin(x**3), 1/3)

print(answer_by_formula)