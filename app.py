import telebot
from telebot import types
from config import currencies, TOKEN
from extensions import ConvertionException, CryptoConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_menu(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Как я могу начать работу?")
    button2 = types.KeyboardButton("Какие валюты доступны?")
    button3 = types.KeyboardButton("Преобразование валюты")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, text='Вас приветствует приложение для преобразования валют!',
                     reply_markup=markup)


@bot.message_handler(commands=['next'])
def next_step(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button4 = types.KeyboardButton("Ввести следующий запрос")
    button5 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(button4, button5)
    bot.send_message(message.chat.id, text="Ваш выбор?", reply_markup=markup)


@bot.message_handler(content_types=['text', ])
def buttons(message: telebot.types.Message):
    if message.text == "Как я могу начать работу?":
        bot.send_message(message.chat.id, "Для работы приложения введите ваш запрос через пробел в следующем виде: \
\n <Валюта> <В какую валюту преобразовать> <Количество>")
    if message.text == "Какие валюты доступны?":
        text = 'Доступные валюты:'
        for key in currencies.keys():
            text = '\n'.join((text, key,))
        bot.send_message(message.chat.id, text)
    if message.text == "Преобразование валюты":
        text = 'Введите ваш запрос:'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, convert)
    if message.text == "Ввести следующий запрос":
        text = 'Введите ваш запрос:'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, convert)
    if message.text == "Вернуться в главное меню":
        text = 'Задача выполнена: /start'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, help_menu)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Вы ввели слишком много параметров!')

        quote, base, amount = values
        total_base = CryptoConvertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e} /help')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
        next_text = 'Ваши дальнейшие действия: /next'
        bot.send_message(message.chat.id, next_text)


bot.polling()
