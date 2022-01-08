from googletrans import Translator
import requests
import json
import datetime
import locale
from weather_ru import get_wind
api_weather2 = '1ef59eb8413621790ab7ecc600010dcd'
def weather_info_kg(api_weather, url, city_name):
    params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
    result = requests.get(url, params=params)
    weather = result.json()
    wind_answer = get_wind(int(weather["wind"]['deg']))
    if weather["main"]['temp'] < 0:
        status = "Аба суук!🥶"
    elif weather["main"]['temp'] < 15:
        status = "Аба анча суук эмес 🙄"
    elif weather["main"]['temp'] > 38:
        status = "Аба ысык☀️"
    else:
        status = "Азырынча аба-ырайы эң жакшы!😙"
    global lat
    lat = weather['coord']['lat']
    global lon
    lon = weather['coord']['lon']
    
    kotoruuchu = Translator() # Translator bu maxsus klass (tarjimon esa obyekt)
    text1 = str(weather['weather'][0]["description"])
    kotor = kotoruuchu.translate(text1, src='ru', dest='ky')
    
    answer = str(city_name) + " шаарында: \n\n"
    answer += "Азыркы учурда " + kotor.text +"\n\n"
    answer += "Температура " + str(int(weather["main"]['temp'])) + " °C\n\n"
    answer += "Сезилген температура " + str(int(weather["main"]['feels_like'])) + " °C\n\n"
    answer += "Шамал: " + wind_answer + str(round(float(weather['wind']['speed']),1)) + " м / сек\n\n"
    answer += "Абанын басымы " + str(round(int(weather['main']['pressure'])*0.75,0)) + " мм рт.ст.\n\n"
    answer += "Абанан нымдуулугу " + str(int(weather['main']['humidity'])) + "%" + "\n\n"
    answer += "Көрүнүү абалы " + str(int(weather['visibility']/1000)) + " км\n\n"
    answer += "Булуттуулук " + str(int(weather["clouds"]['all'])) + " %" + "\n\n" + status
    params.clear()
    return answer, lat , lon
def get_weekly_info_kg(lat, lon, city, lang):
    url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=%s" % (
        lat, lon, api_weather2, lang)
    result1 = requests.get(url2)
    weather1 = json.loads(result1.text)
    locale.setlocale(locale.LC_ALL, "ru")
    now = datetime.datetime.now()
    one_day = datetime.timedelta(1)
    answer = str(city) + " шаарында: \n\n"
    for line in weather1["daily"]:
        wind_answer1 = get_wind(int(line['wind_deg']))
        
        # Рус тилиндеги сөздү кыргыз тилине которуу 
        
        kotoruuchu = Translator() 
        text1 = str((line['weather'][0]['description']))
        kotor = kotoruuchu.translate(text1, src='ru', dest='ky')
    
        answer += now.strftime("%a") + ", " + now.strftime("%d/%m") + ":  " + str(int((line['temp']['max']))) + "/" + str(
            int((line['temp']['min']))) + "°C, " + kotor.text + ", " + str(
            wind_answer1) + str(round(float(line["wind_speed"]),1)) + " м/с\n\n"
        now = now + one_day
        text1 = ""
    return answer
def clear_phrase_kg(phrase):
    phrase = phrase.strip()
    phrase = phrase.lower()
    alphabet_ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    phrase = phrase.replace('ү', 'у')
    phrase = phrase.replace('ө', 'о')
    phrase = phrase.replace('ң', 'н')
    phrase = ''.join(symbol for symbol in phrase if symbol in alphabet_ru)
    phrase = phrase.title()
    return phrase