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
A = (5, 10)