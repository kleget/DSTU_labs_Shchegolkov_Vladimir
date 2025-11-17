with open('input.txt', "r") as file:
    t = file.read()
    t = t.split(' ')
    t0 = int(t[0])
    t1 = int(t[1])

with open('output.txt', 'w') as fl:
    i = t0+t1
    fl.write(str(i))
    