"""
Модуль для запуска приложения прогноза погоды.

Этот модуль отвечает за запуск основного цикла программы,
обновления данных о погоде и взаимодействие с пользовательским интерфейсом.
"""

import asyncio
import sys

from Settings.config import wind_rose, sqlite_database
from Settings.utils import get_city_coordinates
from Database.db_manager import DataBaseManager
from Tools.extractor import DataService
from Tools.upd_weather import update_weather
from Interface.interface import UserInterface as UI
from Interface.messages import city_message


async def main():
    # Конфигурация города
    city, latitude, longitude = await get_city_coordinates()
    print(city_message(city))

    # Запуск обновления погоды в отдельном таске
    asyncio.create_task(update_weather(city, latitude, longitude))

    # Запуск интерфейса пользователя
    MNG = DataBaseManager(sqlite_database)
    ui = UI(MNG)
    await ui.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВыполнение прервано пользователем.")
    except Exception as e:
        print(f"\nОшибка main: {e}")
