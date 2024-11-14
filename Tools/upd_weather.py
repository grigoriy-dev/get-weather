import asyncio
from Database.base import Weather
from Database.db_manager import DataBaseManager
from Tools.extractor import DataService
from Settings.config import delay, cities, wind_rose, sqlite_database


async def update_weather(city, latitude, longitude):
    while True:
        # Ждем delay минут перед следующим обновлением
        await asyncio.sleep(delay * 60)
        try:
            MNG = DataBaseManager(sqlite_database)
            DS = DataService(latitude, longitude)

            raw_data = await DS.fetch_data()
            transform_data = await DS.transform_data(raw_data, city)
            load_data = await MNG.save_weather(weather=transform_data)
            print('Данные успешно сохранены в БД')
        except Exception as e:
            print(f"Произошла ошибка при обновлении погоды: {e}")
        