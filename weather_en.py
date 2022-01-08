import requests
import json
import datetime
from weather_ru import get_wind
api_weather2 = '1ef59eb8413621790ab7ecc600010dcd'
def weather_info_en(api_weather, url, city_name, lang):
    params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': lang}
    result = requests.get(url, params=params)
    weather = result.json()
    wind_answer = get_wind(int(weather["wind"]['deg']))
    if weather["main"]['temp'] < 0:
        status = "It's too cold!🥶"
    elif weather["main"]['temp'] < 15:
        status = "It's cool now!🙄"
    elif weather["main"]['temp'] > 38:
        status = "It's hot now!☀️"
    else:
        status = "Now the temperature is great! 😙"
    global lat_en
    lat_en = weather['coord']['lat']
    global lon_en
    lon_en = weather['coord']['lon']
    answer = "In the city " + str(city_name) + ":\n\n"
    answer += "Temperature is " + str(int(weather["main"]['temp'])) + " °C\n\n"
    answer += "Feels like " + str(int(weather["main"]['feels_like'])) + " °C\n\n"
    answer += "Description: " + str(weather['weather'][0]["description"]) + "\n\n"
    answer += "The wind: " + wind_answer +str(round(float(weather['wind']['speed']),1)) + " m/s\n\n"
    answer += "Pressure " + str(int(weather['main']['pressure'])) + "hPa\n\n"
    answer += "Humidity " + str(int(weather['main']['humidity'])) + "%" + "\n\n"
    answer += "Visibility " + str(int(weather['visibility']/1000)) + " km\n\n"
    answer += "Cloudiness " + str(int(weather["clouds"]['all'])) + " %" + "\n\n" + status
    return answer, lat_en, lon_en
def get_weekly_info_en(lat, lon, city):
    url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&" % (
        lat, lon, api_weather2)
    result1 = requests.get(url2)
    weather1 = json.loads(result1.text)

    now = datetime.datetime.now()
    one_day = datetime.timedelta(1)
    answer = "In the city " + str(city) + ":" + "\n\n"
    for line in weather1["daily"]:
        wind_answer1 = get_wind(int(line['wind_deg']))
        answer += now.strftime("%a") + ", " + now.strftime("%d/%m") + ":  " + str(int((line['temp']['max']))) + "/" + str(
            int((line['temp']['min']))) + "°C, " + str((line['weather'][0]['description'])) + ", " + str(
            wind_answer1) + str(round(float(line["wind_speed"]),1)) + " м/с\n\n"
        now = now + one_day
    return answer
def get_manual():
    text = 'I am a simple bot to show the weather. Choose the language you need and write the name of the city. '\
            'I can show both current and weekly weather. \n Make sure you spell the city name correctly ' \
            'in the selected language, otherwise I cannot find the city ☹️. If you have any problems or questions, write to us 🖊: \n'\
            '@Adilett_B\n@Kuzikaev\nYou should understand that some cities cannot be in my database. \n' \
            'Sometimes commands need to be sent twice 😜. Enjoy your use 😇 \n '
    return text
def clear_phrase_en(phrase):
    phrase = phrase.strip()
    phrase = phrase.lower()
    alphabet_en = 'qwertyuiopasdfghjklzxcvbnm- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet_en)
    result = result.title()
    return result