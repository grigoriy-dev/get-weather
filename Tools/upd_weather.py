"""
Модуль для обновления данных о погоде.

Этот модуль отвечает за регулярное обновление данных о погоде
в заданный промежут времени {delay} для заданного города {city}.
Данные извлекаются через API, преобразуются и сохраняются в базу данных.
"""

import asyncio

from Database.base import Weather
from Database.db_manager import DataBaseManager
from Tools.extractor import DataService
from Settings.config import delay, wind_rose, sqlite_database


async def update_weather(city: str, latitude: float, longitude: float):
    """
    Функция для регулярного обновления данных о погоде.
    """
    while True:
        # Создаем экземпляры менеджера базы данных и сервиса извлечения данных
        mng = DataBaseManager(sqlite_database)
        ds = DataService(latitude, longitude)

        # Извлекаем, Преобразуем, Сохраняем данные
        raw_data = await ds.fetch_data()
        transformed_data = await ds.transform_data(raw_data, city)
        await mng.save_weather(transformed_data)

        # Ожидаем delay минут перед следующим обновлением
        await asyncio.sleep(delay * 60)
        