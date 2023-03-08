import db_handler
import tools
import telebot
import datetime

token = '6013269021:AAEHCmN6I2lvXW6Q6jsNLy4GUSllbYCXF3g'

bot = telebot.TeleBot(token)

today = datetime.date.today()
current_week = today.isocalendar()[1]
type_week = current_week % 2


@bot.message_handler(commands=['start'])
def start(message):
    # keyboard = types.ReplyKeyboardMarkup()
    # keyboard.add("Понедельник", "Вторник")
    # keyboard.add("Среда", "Четверг")
    # keyboard.add("Пятница", "Суббота")
    # keyboard.add("Расписание на текущую неделю")
    # keyboard.add("Расписание на следующую неделю")
    bot.send_message(message.chat.id,
                     'Приветствую! Не забудьте заглянуть в /help, чтобы ознакомиться со мной поподробней.')
    # reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = "Я — первый чат-бот, написаный Александром Хохловым.\n"
    help_text += "Я подскажу вам расписание занятий группы БВТ2204.\n\n"
    help_text += "Вот список доступных команд:\n\n"
    help_text += "/start - начать работу с ботом\n"
    help_text += "/help - получить помощь\n"
    help_text += "/monday - расписание на понедельник\n"
    help_text += "/tuesday - расписание на вторник\n"
    help_text += "/wednesday - расписание на среду\n"
    help_text += "/thursday - расписание на четверг\n"
    help_text += "/friday - расписание на пятницу\n"
    help_text += "/saturday - расписание на субботу\n"
    help_text += "/week - расписание на текущую неделю\n"
    help_text += "/next_week - расписание на следующую неделю\n"
    help_text += "/mtusi - это вам предстоит проверить\n"
    help_text += "/type_week - выводит, какая сейчас неделя\n"

    bot.send_message(message.chat.id, help_text)


@bot.message_handler(func=lambda message: message.text.lower() in tools.weekdays())
@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def one_day(message):
    global type_week
    day = message.text
    if day[0] == '/':
        day = tools.convert_weekday(day[1:])
    timetable_day = db_handler.day_handler(day, type_week)
    bot.send_message(message.chat.id,
                     f"{tools.get_week_type(type_week).title()} ({current_week - 4})\n{'-' * 50}\n{timetable_day}\n")


@bot.message_handler(commands=['week'])
@bot.message_handler(func=lambda message: message.text == 'Расписание на текущую неделю')
def week(message):
    global type_week

    timetable = db_handler.week_handler([type_week, current_week - 4])
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['next_week'])
@bot.message_handler(func=lambda message: message.text == 'Расписание на следующую неделю')
def next_week(message):
    global type_week
    if not type_week:
        timetable = db_handler.week_handler([type_week + 1, current_week - 3])
        bot.send_message(message.chat.id, timetable)
    else:
        timetable = db_handler.week_handler([type_week - 1, current_week - 3])
        bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['mtusi'])
def abs(message):
    bot.send_message(message.chat.id, 'официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(commands=['type_week'])
def week_type(message):
    global type_week

    bot.send_message(message.chat.id, f'сейчас {tools.get_week_type(type_week)} ({current_week - 4})')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id,
                         f'И вам Здравствуйте, {message.from_user.first_name}\n '
                         f'Или к вам лучше обращаться {message.from_user.username}')
    else:
        bot.send_message(message.chat.id,
                         'Я всего лишь чат-бот с расписанием. Лучше откройте меню и выберите то, что вам нужно.')


bot.polling(none_stop=True)
