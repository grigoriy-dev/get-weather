"""
Модуль для вспомогательных функций:

round_value - Округление по математическим правилам
get_wind_direction - Определение направления ветра по значению угла
get_city_coordinates - Извлечение координат города по названию
"""

import json
import asyncio
from math import ceil, floor

from Settings.config import wind_rose, cities_path


async def round_value(value):
    """
    Функция использует математические правила округления: 
    если дробная часть больше или равна 0.5, то значение округляется вверх, иначе вниз.
    """
    if value % 1 >= 0.5:
        return ceil(value)
    else:
        return floor(value)

async def get_wind_direction(wind_grade):
    """
    Определение направления ветра по значению угла.
    Находит направление ветра из списка направлений, используя розу ветров {wind_rose}.
    """
    rose = wind_rose
    return rose[min(rose, key=lambda x: abs(x - wind_grade))]

async def get_city_coordinates():
    """
    Извлечение координат города по названию {city}.
    Функция использует бесконечный цикл while True, который продолжается до тех пор, пока не будет выполнен выход из него через return
    """
    while True:
        city = input('Введите название города: ')
        with open(cities_path, 'r') as f:
            data = json.load(f)
        if city in data:
            return city, *data[city]
        else:
            print("Город не найден. Попробуйте еще раз.")
