with open('first.txt', 'r', encoding='utf-8') as f:
    a = f.readlines()
    a = list(a[0])
    a = sorted(a)

answ = {}
for x in range(len(a)):
    if a[x].isupper():
        if a[x] not in answ:
            answ[a[x]] = 1
        else:
            answ[a[x]] +=1

with open('result.txt', 'w', encoding='utf-8') as file:
    for x in answ:
        file.write(f'{x}-{answ[x]}\n')


##############################################

with open('second.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

with open('second.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        words = line.split()
        to_remove = [i for i, word in enumerate(words) if 3 <= len(word) <= 5]
        to_remove = to_remove[:len(to_remove) - len(to_remove) % 2]
        new_line = ' '.join(word for i, word in enumerate(words) if i not in to_remove)
        file.write(new_line + '\n')