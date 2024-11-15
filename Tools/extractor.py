"""
Модуль для обработки данных о погоде.

Этот модуль предоставляет классы и методы для взаимодействия с API погоды,
преобразования полученных данных и формирования объектов для хранения информации о погоде.
"""

import asyncio
import aiohttp
from typing import Dict, Any

from Database.base import Weather
from Settings.config import precipitation_map
from Settings.utils import round_value, get_wind_direction


class DataService:
    """
    Класс для работы с данными о погоде.
    Осуществляет запрос к API, преобразование полученных данных и формирование объекта Weather.
    """
    def __init__(self, latitude: float, longitude: float):
        # Конструктор класса
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "rain", "showers",
                "snowfall",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m"
            ],
            "timezone": "Europe/Moscow",
            "wind_speed_unit": "ms",
            "forecast_days": 1
        }

    async def fetch_data(self) -> Dict[str, Any]:
        # Асинхронный метод для получения сырых данных о погоде с API.
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed. Status code: {response.status}")

    async def transform_data(self, raw_data: Dict[str, Any], city: str) -> Weather:
        # Метод для преобразования сырых данных в объект класса Weather.
        raw_data = raw_data['current']
        transformed_data = {
            'city': city,
            'date': raw_data['time'][:10],
            'time': raw_data['time'][11:],
            'temperature': await round_value(raw_data['temperature_2m']),
            'wind_dir': await get_wind_direction(raw_data['wind_direction_10m']),
            'wind_speed': await round_value(raw_data['wind_speed_10m']),
            'pressure': await round_value(raw_data['surface_pressure'])
        }

        for key, (prec_type, amount_key) in precipitation_map.items():
            if key in raw_data:
                transformed_data['precipitation'] = prec_type
                transformed_data['prec_amount'] = raw_data[amount_key]
                break
        else:
            transformed_data['precipitation'] = 'Без осадков'
            transformed_data['prec_amount'] = 0

        return Weather(**transformed_data)

    async def get_weather(self, city: str) -> Weather:
        # Объединяет вызов всех остальных методов и возвращает объект Weather.
        raw_data = await self.fetch_data()
        current_data = raw_data["current"]
        return await self.transform_data(current_data, city)
