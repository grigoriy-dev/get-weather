from Settings.config import cities, wind_rose, sqlite_database
from Database.db_manager import DataBaseManager
from Tools.extractor import DataService
from Tools.upd_weather import update_weather
from Interface.interface import UserInterface as UI
from Interface.messages import city_message

import asyncio
import sys
import traceback


async def main():
    city = "Москва"
    latitude, longitude = cities[city]

    print(city_message(city))

    MNG = DataBaseManager(sqlite_database)
    DS = DataService(latitude, longitude)

    raw_data = await DS.fetch_data()
    transform_data = await DS.transform_data(raw_data, city)
    load_data = await MNG.save_weather(weather=transform_data)
    ui = UI(MNG)

    # Запуск обновления погоды в отдельном таске
    asyncio.create_task(update_weather(city, latitude, longitude))

    # Запуск интерфейса пользователя
    await ui.run()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("\nВыполнение прервано пользователем.")
    except Exception as e:
        print(f"\nОшибка: {e}")
