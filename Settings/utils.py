"""
Модуль для вспомогательных функций.
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

async def get_city_coordinates(city):
    """
    Извлечение координат города по названию {city}.
    """
    with open(cities_path, 'r') as f:
        data = json.load(f)
    return data[city]
