text = 'Мишинка БМВ обогнала мерс на скорости чик чирик'
text = text.split(' ')
text = set(text)
a = {'БМВ', 'мерс', 'ауди'}
print(text.intersection(a))