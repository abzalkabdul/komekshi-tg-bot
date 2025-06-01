import telebot
import requests
import json

# bot = telebot.TeleBot('8037509589:AAFYpACnb_rYTExhmTtUTew1Q391IQfd6Nk')
API = '6e0e43043f17c564eca6f26d1c1f8473'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]

        image = 'sun.png' if temp > 5.0 else 'sunny.png'
        file = open(f'./{image}', 'rb')
        bot.send_photo(message.chat.id, file)

        bot.reply_to(message, f'Сейчас температура: {temp} C°')
    else:
        bot.send_message(message.chat.id, 'Город указан не верно')

     

bot.polling(none_stop=True)