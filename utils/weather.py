#!/usr/bin/env python
import requests
import json
import sys


class weather:
    def __init__(self, city_name):
        info = get_info(city_name)
        self.name = info['name']
        self.country = info['sys']['country']
        self.dt = info['dt']
        self.temp = info['main']['temp']
        self.temp_min = info['main']['temp_min']
        self.temp_max = info['main']['temp_max']
        self.pressure = info['main']['pressure']
        self.humidity = info['main']['humidity']
        weather = info['weather']
#        self.sky = weather[0].values()[0] + ':' + weather[0].values()[3]
        self.wind = info['wind']['speed']
        self.cloud = info['clouds']['all']


    def get_info(city_name):
        query = 'http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&&APPID=7eaa0cd93aca93f3ff4c382a5c17d61c' % city_name
        r = requests.get(query)
        result = json.loads(r.text)
        if result['cod'] == '404':
            print('Error:city not found,please check name of city', sys.exit())
        else:
            return result

class forecast:
    def __init__(self, city_name):
        info = get_info(city_name)
        self.name = city_name
        #self.country = info['sys']['country']
        self.dt = info['dt_txt']
        self.temp = info['main']['temp']
        self.temp_min = info['main']['temp_min']
        self.temp_max = info['main']['temp_max']
        self.pressure = info['main']['pressure']
        self.humidity = info['main']['humidity']
        weather = info['weather']
        self.main_weather = weather[0]['main']
        self.weather_description = weather[0]['description']
        self.wind = info['wind']['speed']
        print(self.wind)
        self.cloud = info['clouds']['all']


    def get_info(city_name):
        query = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&units=metric&&APPID=7eaa0cd93aca93f3ff4c382a5c17d61c' % city_name
        r = requests.get(query)
        result = json.loads(r.text)
        elemento = result['list']
        print(elemento[1])
        if result['cod'] == '404':
            print
            'Error:city not found,please check name of city', sys.exit()
        else:
            return elemento[1]