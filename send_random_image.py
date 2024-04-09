import requests  # Импортируем библиотеку для работы с запросами

from telegram import Bot

bot = Bot(token='5697391909:AAGuHPmOIj7Y6MlFMIsfFUKoom7PpDS3T9c')
# Адрес API сохраним в константе
URL = 'https://api.thecatapi.com/v1/images/search'
chat_id = 5719638632
# Сделаем GET-запрос к API
# метод json() преобразует полученный ответ JSON в тип данных, понятный Python
response = requests.get(URL).json()
# Рассмотрим структуру и содержимое переменной response
print(response)
# Посмотрим, какого типа переменная response
print(type(response))
# response - это список. А какой длины?
print(len(response))
# Посмотрим, какого типа первый элемент
print(type(response[0])) 

# Извлекаем из ответа URL картинки:
random_cat_url = response[0].get('url')
# Передаём chat_id и URL картинки в метод для отправки фото:
bot.send_photo(chat_id, random_cat_url) 

