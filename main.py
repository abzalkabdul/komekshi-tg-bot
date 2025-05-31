import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('8037509589:AAFYpACnb_rYTExhmTtUTew1Q391IQfd6Nk')
name = ''


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('first.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id integer primary key autoincrement, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    file = open('./photo.png', 'rb') 
    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, 'Привет, давай я тебя зарегаю. Введите имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('first.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users(name, pass) VALUES(?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='lst_users'))

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован !', reply_markup=markup)


@bot.message_handler(commands=['func_btns'])
def func_btns(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Go to website', callback_data='goto')
    btn2 = types.KeyboardButton('Say Hello', callback_data='sayhello')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'lst_users':
        
        conn = sqlite3.connect('first.sql')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()

        info = ''
        for el in users:
            info += f'Имя: {el[1]}, Пароль: {el[2]}\n'

        bot.send_message(callback.message.chat.id, info)
    elif callback.data == 'goto':
        webbrowser.open('https://kaspi.kz')
    elif callback.data == 'sayhello':
        bot.send_message(callback.message.chat.id, 'No.')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://kaspi.kz')

@bot.message_handler(commands=['main', 'hello'])
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



bot.polling(none_stop=True)

