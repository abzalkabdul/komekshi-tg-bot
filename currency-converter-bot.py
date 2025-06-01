import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('8037509589:AAFYpACnb_rYTExhmTtUTew1Q391IQfd6Nk')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, укажите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.reply_to(message, 'Неверный формат, Впишите сумму', reply_markup=markup)
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/GBP')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.reply_to(message, 'Выберите конвертацию', reply_markup=markup)
    else: 
        bot.send_message(message.chat.id, 'Число должно быть больше нуля !')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получится: {round(res, 2)}. Можете заново сконвертировать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получится: {round(res, 2)}. Можете и дальше конвертировать эту же сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Что то не так, впишите сумму заново')
        bot.register_next_step_handler(message, summa)



bot.polling(none_stop=True)