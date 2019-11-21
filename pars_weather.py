from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import requests

global city_name
appid = "96b3571387d7b8e0d5b71b4a15a00029"
weather_values = []
city_name = 'минск'
class CityForm(FlaskForm):              #форма указания города на html странице
    city = StringField('Введите город:', validators=[DataRequired()])
    submit = SubmitField('Искать!')

def find_id(city_name):                 #поиск id города
    city_id = 0
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                params={'q': city_name, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json() 
    city_id = data['list'][0]['id']
    return city_id


def wheather_now(city_name):            #погода сейчас
    weather_values = []
    city_id = find_id(city_name)
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        weather_values = ((data['weather'][0]['description']).capitalize(),f"сейчас: {data['main']['temp']}°")
        return weather_values

        
    except Exception as e:
        print("Exception (weather):", e)
        pass

def hourly_weather(city_name):              #почасовая погода, правый столбик
    weather_list = []
    city_id = find_id(city_name)
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            lis = f"{i['dt_txt']}  t {round(i['main']['temp'])}°. {(i['weather'][0]['description']).capitalize()}"
            weather_list.append(lis)
        return weather_list
    except Exception as e:
        print("Exception (forecast):", e)


hourly_weather(city_name)

# def get_now_url(city_name):
#     url_city = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID=96b3571387d7b8e0d5b71b4a15a00029"
#     return url_city

# def show_weather(city_name):
    
#     weather_values = []
#     response = requests.get(get_now_url(city_name)).json()
#     temp = f"Сейчас  {round(response['main']['temp']-273.15)}°"
#     temp_min = f"Минимальная  {round(response['main']['temp_min']-273.15)}°"
#     temp_max = f"Максимальная  {round(response['main']['temp_max']-273.15)}°"
#     humidity = f"Влажность  {response['main']['humidity']}%"
    
#     weather_values.extend([temp, temp_min, temp_max, humidity])
#     return weather_values

    
