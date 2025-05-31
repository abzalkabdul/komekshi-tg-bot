import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot('8037509589:AAFYpACnb_rYTExhmTtUTew1Q391IQfd6Nk')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('smth1')
    btn2 = types.KeyboardButton('smth2')
    btn3 = types.KeyboardButton('smth3')
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://kaspi.kz')

@bot.message_handler(commands=['start', 'main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name} !!!')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>please</u></em>!!!', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'hello':
        bot.send_message(
            message.chat.id, f'hi {message.from_user.first_name} !')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Your id is {message.from_user.id}')
        

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Search it in google !', url='https://google.com')
    btn2 = types.InlineKeyboardButton('Edit smth', callback_data='edit')
    btn3 = types.InlineKeyboardButton('Delete a photo', callback_data='delete')
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.reply_to(message, 'What a beautiful photo !', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)

