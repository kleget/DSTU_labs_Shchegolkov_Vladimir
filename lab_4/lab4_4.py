# задание 15

seconds = int(input('Введите колличество секунд: '))
answer = 0
if seconds >= 86400:
    answer = f'Дни: {seconds//86400}\nЧасы: {(seconds%86400)//3600}\nМинуты: {((seconds%86400)%3600)//60}\nСекунды: {((seconds%86400)%3600)%60}'
elif seconds >= 3600:
    answer = f'Часы: {(seconds%86400)//3600}\nМинуты: {((seconds%86400)%3600)//60}\nСекунды: {((seconds%86400)%3600)%60}'
elif seconds >= 60:
    answer = f'Минуты: {((seconds%86400)%3600)//60}\nСекунды: {((seconds%86400)%3600)%60}'
elif seconds < 60:
    answer = f'Минуты: {((seconds%86400)%3600)//60}\nСекунды: {((seconds%86400)%3600)%60}'
else:
    answer = 'Билиберда'
print(answer)


