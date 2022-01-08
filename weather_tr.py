import requests
import json
import datetime
from weather_ru import get_wind
import locale

api_weather2 = '1ef59eb8413621790ab7ecc600010dcd'
def weather_info_tr(api_weather, url, city_name, lang):
    params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'tr'}
    result = requests.get(url, params=params)
    weather = result.json()
    wind_answer = get_wind(int(weather["wind"]['deg']))
    if weather["main"]['temp'] < 0:
        status = "Hava çok soğuk!🥶"
    elif weather["main"]['temp'] < 15:
        status = "Hava serin 🙄"
    elif weather["main"]['temp'] > 38:
        status = "Hava sıcak☀️"
    else:
        status = "Şimdi hava harika!😙"
    global lat
    lat = weather['coord']['lat']
    global lon
    lon = weather['coord']['lon']
    answer = str(city_name) + " şehrinde:\n\n"
    answer += "Şimdi " + str(weather['weather'][0]["description"]) + "\n\n"
    answer += "Sıcaklık " + str(int(weather["main"]['temp'])) + " °C\n\n"
    answer += "Hissedilen sıcaklık: " + str(int(weather["main"]['feels_like'])) + " °C\n\n"
    answer += "Rüzgar: " + wind_answer + str(round(float(weather['wind']['speed']),1)) + " m/s hızla esiyor \n\n"
    answer += "Basınç " + str(int(weather['main']['pressure'])) + "hPa\n\n"
    answer += "Nem %" + str(int(weather['main']['humidity'])) + "\n\n"
    answer += "Görünürlük: " + str(int(weather['visibility']/1000)) + " km\n\n"
    answer += "Bulutluluk %" + str(int(weather["clouds"]['all'])) + "\n\n" + status
    params.clear()
    return answer, lat , lon
def get_weekly_info_tr(lat, lon, city, lang):
    url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&lang=%s" % (
        lat, lon, api_weather2, lang)
    result1 = requests.get(url2)
    weather1 = json.loads(result1.text)
    locale.setlocale(locale.LC_ALL, "tr")
    now = datetime.datetime.now()
    one_day = datetime.timedelta(1)
    answer = str(city) + " şehrinde:\n\n"
    for line in weather1["daily"]:
        wind_answer1 = get_wind(int(line['wind_deg']))
        answer += now.strftime("%a") + ", " + now.strftime("%d/%m") + ":  " + str(int((line['temp']['max']))) + "/" + str(
            int((line['temp']['min']))) + "°C, " + str((line['weather'][0]['description'])) + ", " + str(
            wind_answer1) + str(round(float(line["wind_speed"]),1)) + " м/с\n\n"
        now = now + one_day
    return answer

def clear_phrase_tr(phrase):
    phrase = phrase.strip()
    phrase = phrase.lower()
    alphabet_en = 'çğıöşüertyuiopasdfghjklzcvbnm- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet_en)
    result = result.title()
    return result