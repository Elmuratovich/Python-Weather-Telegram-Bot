import requests
import json
import datetime
import locale
api_weather2 = '1ef59eb8413621790ab7ecc600010dcd'
def weather_info_ru(api_weather,url , city_name, lang):
    params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': lang}
    result = requests.get(url, params=params)
    weather = result.json()
    wind_answer = get_wind(int(weather["wind"]['deg']))
    if weather["main"]['temp'] < 0:
        status = "Сейчас холодно!🥶"
    elif weather["main"]['temp'] < 10:
        status = "Терпимо!😬"
    elif weather["main"]['temp'] < 15:
        status = "Прохладно!🙄"
    elif weather["main"]['temp'] > 30:
        status = "Сейчас жарко!☀️"
    else:
        status = "Сейчас отличная температура! 😙"
    global lat
    lat = weather['coord']['lat']
    global lon
    lon = weather['coord']['lon']
    answer = "В городе " + str(city_name) + ":\n\n"
    answer += "Сейчас " + str(weather['weather'][0]["description"]) + "\n\n"
    answer += "Температура " + str(int(weather["main"]['temp'])) + " °C\n\n"
    answer += "Чувствуется как " + str(int(weather["main"]['feels_like'])) + " °C\n\n"
    answer += "Ветер: " + wind_answer + str(float(weather['wind']['speed'])) + " м/сек\n\n"
    answer += "Давление " + str(round(int(weather['main']['pressure'])*0.75,0)) + " мм рт.ст.\n\n"
    answer += "Влажность " + str(int(weather['main']['humidity'])) + "%" + "\n\n"
    answer += "Видимость " + str(int(weather['visibility']/1000)) + " км\n\n"
    answer += "Облачность " + str(int(weather["clouds"]['all'])) + " %" + "\n\n" + status
    return answer, lat , lon

def get_weekly_info_ru(lat, lon, city, lang):
    url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=%s" % (
        lat, lon, api_weather2, lang)
    result1 = requests.get(url2)
    weather1 = json.loads(result1.text)
    locale.setlocale(locale.LC_ALL, "ru")
    now = datetime.datetime.now()
    one_day = datetime.timedelta(1)
    answer = "В городе " + str(city) + ":" + "\n\n"
    for line in weather1["daily"]:
        wind_answer1 = get_wind(int(line['wind_deg']))
        answer += now.strftime("%a") + ", " + now.strftime("%d/%m") + ":  " + str(int((line['temp']['max']))) + "/" + str(
            int((line['temp']['min']))) + "°C, "+str((line['weather'][0]['description']))+", "+str(
            wind_answer1)+str(round(float(line["wind_speed"]),1))+" м/с\n\n"
        now = now + one_day
    return answer
    del answer
def get_manual():
    text = 'Я простой бот показывающий погоду. Выбери нужный тебе язык и напиши название города. ' \
           'Могу показать как текущую так и недельную погоду.\nУбедись в том, что правильно написал название города ' \
           'в выбронном языке, в противном случае я не смогу найти город ☹️. Если возникли проблемы и вопросы напишите нам 🖊:\n' \
           '@Adilett_B\n@Kuzikaev\nВы должны понять, что некоторые города не могут быть в моём базе данных.\n ' \
           'Иногда команды нужно отправлять два раза 😜.\n Приятного использования 😇'
    return  text
def get_wind(wind):
    if 23 <= wind < 68:
        wind_answer = " ↙️ "
    elif 68 <= wind < 112:
        wind_answer = " ⬅️ "
    elif 112 <= wind < 157:
        wind_answer = " ↖️ "
    elif 157 <= wind < 202:
        wind_answer = " ⬆️ "
    elif 202 <= wind < 247:
        wind_answer = " ↗️ "
    elif 247 <= wind < 292:
        wind_answer = " ➡️ "
    elif 292 <= wind < 337:
        wind_answer = " ↘️ "
    else:
        wind_answer = " ⬇️ "
    return wind_answer

def clear_phrase_ru(phrase):
    old_name = phrase.strip()
    phrase = old_name.lower()
    alphabet_ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet_ru)
    result = result.title()
    return result