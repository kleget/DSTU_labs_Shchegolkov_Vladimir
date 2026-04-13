import numpy as np
from math import exp, factorial

# данные (вариант 13)
x = np.array([0,1,2,3,4,5,6])
n = np.array([62,45,22,16,8,4,2])
N = n.sum()

# 1. lambda
lam = (x * n).sum() / N

# 2. вероятности (без округления!)
p = np.array([exp(-lam) * lam**k / factorial(k) for k in x])

# 3. теоретические частоты
n_theor = N * p

# 4. ОБЪЕДИНЕНИЕ (как руками)
# объединяем 4,5,6
obs = np.array([
    n[0],
    n[1],
    n[2],
    n[3],
    n[4] + n[5] + n[6]
])

theor = np.array([
    n_theor[0],
    n_theor[1],
    n_theor[2],
    n_theor[3],
    n_theor[4] + n_theor[5] + n_theor[6]
])

# 5. хи-квадрат
chi2 = ((obs - theor)**2 / theor).sum()

print("lambda =", lam)
print("chi2 =", chi2)