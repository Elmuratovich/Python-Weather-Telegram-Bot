
import telebot
from telebot import types
from weather_ru import weather_info_ru
from weather_ru import clear_phrase_ru
from weather_ru import get_weekly_info_ru
import weather_ru
from weather_en import weather_info_en
from weather_en import clear_phrase_en
from weather_en import get_weekly_info_en
import weather_en
from weather_tr import weather_info_tr
from weather_tr import clear_phrase_tr
from weather_tr import get_weekly_info_tr
import weather_tr
from weather_kg import weather_info_kg
from weather_kg import clear_phrase_kg
from weather_kg import get_weekly_info_kg
import weather_kg
api_weather = '5b67cb156ecfee9cdeafdabe9db6975f'
url = 'http://api.openweathermap.org/data/2.5/weather'

api_telegram = '1546369114:AAHbyzVp1V-DL-oVG722gHQESNZFUYVBKLc'
bot = telebot.TeleBot(api_telegram)
metka = False
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                           "Привет " + message.from_user.first_name + ", 🤗 я бот погода\n\nHi " +
                           message.from_user.first_name + ", I'm weather bot\n")
    bot.send_message(message.chat.id, welcome_lang(message))
@bot.message_handler(commands=['changelanguages'])
def change_lang(message):
    bot.send_message(message.chat.id, welcome_lang(message))
def welcome_lang(message):
    a = message.text
    markup = types.ReplyKeyboardRemove(selective=False)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('🇰🇬 KG')
    itembtn2 = types.KeyboardButton('🇹🇷 TR')
    itembtn3 = types.KeyboardButton('🇷🇺 RU')
    itembtn4 = types.KeyboardButton('🇬🇧 EN')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, "Выберите язык / Choose language:\n", reply_markup=markup)
    bot.register_next_step_handler(msg, type_the_city)
def type_the_city(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    global lang
    if (message.text == '🇰🇬 KG'):
        lang = 'ru'
        bot.send_message(message.chat.id, "Тандалган тил: Кыргыз тили")
        msg = bot.send_message(message.chat.id, "Шаарды киргизиңиз:")
        bot.register_next_step_handler(msg, choose_the_day_kg)
    elif (message.text == "🇷🇺 RU"):
        lang = 'ru'
        bot.send_message(message.chat.id, "Выбран язык: Русский")
        msg = bot.send_message(message.chat.id, "Введите город:")
        bot.register_next_step_handler(msg, choose_the_day_ru)

    elif (message.text == "🇹🇷 TR"):
        lang = 'tr'
        bot.send_message(message.chat.id, "Seçilen dil: Türk Dili")
        msg = bot.send_message(message.chat.id, "Şehiri yazınız:")
        bot.register_next_step_handler(msg, choose_the_day_tr)

    elif (message.text == "🇬🇧 EN"):
        lang = 'en'
        bot.send_message(message.chat.id, "Selected language: English")
        msg = bot.send_message(message.chat.id, "Write the city:")
        bot.register_next_step_handler(msg, choose_the_day_en)


@bot.message_handler(commands=['help'])
def welcome(message):
    text_ru = weather_ru.get_manual()
    text_en = weather_en.get_manual()
    bot.send_message(message.chat.id, text_ru + '\n\n'+text_en+'/start\n/help\n/changelanguages')

def choose_the_day_kg(message):
    global city_kg
    city_kg = message.text
    city_kg = clear_phrase_kg(city_kg)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Азыркы')
    itembtn2 = types.KeyboardButton('Бир жумалык')
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, "Кайсы аба-ырайынын маалыматы керек?", reply_markup=markup)
    bot.register_next_step_handler(msg, choosing)

def choose_the_day_tr(message):
    global city_tr
    city_tr = message.text
    city_tr = clear_phrase_tr(city_tr)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Şu anki')
    itembtn2 = types.KeyboardButton('Haftalık')
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, "Ne tür bir hava ile ilgileniyorsunuz?", reply_markup=markup)
    bot.register_next_step_handler(msg, choosing)

def choose_the_day_en(message):
    global city_en
    city_en = message.text
    city_en = clear_phrase_en(city_en)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Current')
    itembtn2 = types.KeyboardButton('Weekly')
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, "What kind of weather you are interested in?", reply_markup=markup)
    bot.register_next_step_handler(msg, choosing)

def choose_the_day_ru(message):
    global city_ru
    city_ru = message.text
    city_ru = clear_phrase_ru(city_ru)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Текущая')
    itembtn2 = types.KeyboardButton('Недельная')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id, "Какая погода вас интересует?", reply_markup=markup)
    bot.register_next_step_handler(msg, choosing)
def choosing(message):
    if message.text == "Недельная":
        bot.send_message(message.chat.id, send_echo_ru_week(message))
    elif message.text == "Текущая":
        bot.send_message(message.chat.id, send_echo_ru(message))

    elif message.text == "Current":
        bot.send_message(message.chat.id, send_echo_en(message))
    elif message.text == "Weekly":
        bot.send_message(message.chat.id, send_echo_en_week(message))

    elif message.text == "Şu anki":
        bot.send_message(message.chat.id, send_echo_tr(message))
    elif message.text == "Haftalık":
        bot.send_message(message.chat.id, send_echo_tr_week(message))

    elif message.text == "Азыркы":
        bot.send_message(message.chat.id, send_echo_kg(message))
    elif message.text == "Бир жумалык":
        bot.send_message(message.chat.id, send_echo_kg_week(message))
#-----------------------------------------------------------------------------------



def send_echo_ru(message):
    global metka
    metka = False
    try:
        answer = weather_info_ru(api_weather, url, city_ru, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Город  не найден")
    bot.send_message(message.chat.id, next_step_ru(message))
def send_echo_ru_week(message):
    global metka
    metka = True
    try:
        a, lat, lon = weather_info_ru(api_weather, url, city_ru, lang)
        #a.message.delete()
        answer = get_weekly_info_ru(lat, lon, city_ru, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Город  не найден")
    bot.send_message(message.chat.id, next_step_ru(message))
def next_step_ru(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    if metka:
        btn0 = types.KeyboardButton('Текущая')
    else:
        btn0 = types.KeyboardButton('Недельная')
    btn1 = types.KeyboardButton('Новый город')
    btn2 = types.KeyboardButton('Поменять язык')
    markup.add(btn0, btn1, btn2)
    msg = bot.send_message(message.chat.id, "Что вам надо?", reply_markup=markup)
    bot.register_next_step_handler(msg, next_step1_ru)
def next_step1_ru(message):
    if message.text == "Новый город":
        bot.send_message(message.chat.id, next_step2_ru(message))
    elif message.text == "Недельная":
        metka = False
        try:
            answer = get_weekly_info_ru(weather_ru.lat, weather_ru.lon, city_ru, lang)
            bot.send_message(message.chat.id, answer)
            del answer
        except:
            bot.send_message(message.chat.id, "Город  не найден")
        bot.send_message(message.chat.id, next_step_ru(message))
    elif message.text == "Текущая":
        bot.send_message(message.chat.id, send_echo_ru(message))
    elif message.text == "Поменять язык":
        bot.send_message(message.chat.id, welcome_lang(message))

def next_step2_ru(message):
    msg = bot.send_message(message.chat.id, "Введите город")
    bot.register_next_step_handler(msg, choose_the_day_ru)
#------------------------------------------------------



#------------------------------------------------------
def send_echo_kg(message):
    global metka
    metka = False
    try:
        answer = weather_info_kg(api_weather, url, city_kg)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Шаар табылган жок")
    bot.send_message(message.chat.id, next_step_kg(message))
def send_echo_kg_week(message):
    global metka
    metka = True
    try:
        a, lat, lon = weather_info_kg(api_weather, url, city_kg)
        #a.message.delete()
        answer = get_weekly_info_kg(lat, lon, city_kg, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Шаар табылган жок")
    bot.send_message(message.chat.id, next_step_kg(message))
def next_step_kg(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    if metka:
        btn0 = types.KeyboardButton('Азыркы')
    else:
        btn0 = types.KeyboardButton('Бир жумалык')
    btn1 = types.KeyboardButton('Жаңы шаар')
    btn2 = types.KeyboardButton('Тилди алмаштыруу')
    markup.add(btn0, btn1, btn2)
    msg = bot.send_message(message.chat.id, "Сизге эмне керек?", reply_markup=markup)
    bot.register_next_step_handler(msg, next_step1_kg)
def next_step1_kg(message):
    if message.text == "Жаңы шаар":
        bot.send_message(message.chat.id, next_step2_kg(message))
    elif message.text == "Бир жумалык":
        try:
            answer = get_weekly_info_kg(weather_kg.lat, weather_kg.lon, city_kg, lang)
            bot.send_message(message.chat.id, answer)
            del answer
        except:
            bot.send_message(message.chat.id, "Шаар табылган жок")
        bot.send_message(message.chat.id, next_step_kg(message))
    elif message.text == "Азыркы":
        bot.send_message(message.chat.id, send_echo_kg(message))
    elif message.text == "Тилди алмаштыруу":
        bot.send_message(message.chat.id, welcome_lang(message))
def next_step2_kg(message):
    city_kg = ''
    msg = bot.send_message(message.chat.id, "Шаарды киргизиңиз:")
    bot.register_next_step_handler(msg, choose_the_day_kg)
#------------------------------------------------------



#------------------------------------------------------
def send_echo_tr(message):
    global metka
    metka = False
    try:
        answer = weather_info_tr(api_weather, url, city_tr, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Şehir bulunamadı")
    bot.send_message(message.chat.id, next_step_tr(message))
def send_echo_tr_week(message):
    global metka
    metka = True
    try:
        a, lat, lon = weather_info_tr(api_weather, url, city_tr, lang)
        answer = get_weekly_info_tr(lat, lon, city_tr, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "Şehir bulunamadı")
    bot.send_message(message.chat.id, next_step_tr(message))
def next_step_tr(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    if metka:
        btn0 = types.KeyboardButton('Şu anki')
    else:
        btn0 = types.KeyboardButton('Haftalık')
    btn1 = types.KeyboardButton('Yeni şehir')
    btn2 = types.KeyboardButton('Dili değiştir')
    markup.add(btn0, btn1, btn2)
    msg = bot.send_message(message.chat.id, "Neye ihtiyacın var?", reply_markup=markup)
    bot.register_next_step_handler(msg, next_step1_tr)
def next_step1_tr(message):
    if message.text == "Yeni şehir":
        bot.send_message(message.chat.id, next_step2_tr(message))
    elif message.text == "Haftalık":
        try:
            answer = get_weekly_info_tr(weather_tr.lat, weather_tr.lon, city_tr, lang)
            bot.send_message(message.chat.id, answer)
            del answer
        except:
            bot.send_message(message.chat.id, "Şehir bulunamadı")
        bot.send_message(message.chat.id, next_step_tr(message))
    elif message.text == "Şu anki":
        bot.send_message(message.chat.id, send_echo_tr(message))
    elif message.text == "Dili değiştir":
        bot.send_message(message.chat.id, welcome_lang(message))
def next_step2_tr(message):
    city_tr = ''
    msg = bot.send_message(message.chat.id, "Şehiri yazınız")
    bot.register_next_step_handler(msg, choose_the_day_tr)
#------------------------------------------------------



#------------------------------------------------------
def send_echo_en(message):
    global metka
    metka = False
    try:
        answer = weather_info_en(api_weather, url, city_en, lang)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "City not found")
    bot.send_message(message.chat.id, next_step_en(message))
def send_echo_en_week(message):
    global metka
    metka = True
    try:
        a, lat, lon = weather_info_en(api_weather, url, city_en, lang)
        answer = get_weekly_info_en(lat, lon, city_en)
        bot.send_message(message.chat.id, answer)
        del answer
    except:
        bot.send_message(message.chat.id, "City not found")
    bot.send_message(message.chat.id, next_step_en(message))
def next_step_en(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    if metka:
        btn0 = types.KeyboardButton('Current')
    else:
        btn0 = types.KeyboardButton('Weekly')
    btn1 = types.KeyboardButton('New city')
    btn2 = types.KeyboardButton('Change language')
    markup.add(btn0, btn1, btn2)
    msg = bot.send_message(message.chat.id, "What are you need?", reply_markup=markup)
    bot.register_next_step_handler(msg, next_step1_en)
def next_step1_en(message):
    if message.text == "Weekly":
        try:
            answer = get_weekly_info_en(weather_en.lat_en, weather_en.lon_en, city_en)
            bot.send_message(message.chat.id, answer)
            del answer
        except:
            bot.send_message(message.chat.id, "City not found")
        bot.send_message(message.chat.id, next_step_en(message))
    elif message.text == "New city":
        bot.send_message(message.chat.id, next_step2_en(message))
    elif message.text == "Current":
        bot.send_message(message.chat.id, send_echo_en(message))
    elif message.text == "Change language":
        bot.send_message(message.chat.id, welcome_lang(message))

def next_step2_en(message):
    city_en = ''
    msg = bot.send_message(message.chat.id, "Write the city")
    bot.register_next_step_handler(msg, choose_the_day_en)
#------------------------------------------------------

bot.enable_save_next_step_handlers(delay=0)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
