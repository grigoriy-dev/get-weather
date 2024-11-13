import asyncio
from math import ceil, floor
from typing import Any
from geopy.geocoders import Nominatim
from Data_ETL.extractor import DataExtractor
from Data_ETL.loader import DataLoader
from Data_ETL.transformer import DataTransformer
from Database.config import Weather, WeatherDatabase, sqlite_database
from Interface.interface import UserInterface


async def main():
    # Инициализация объектов
    rose = range(0, 361, 45)
    wind = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ', 'С']
    wind_rose = dict(zip(rose, wind))

    database = WeatherDatabase(sqlite_database)
    extractor = DataExtractor(latitude=55.751244, longitude=37.618423)
    transformer = DataTransformer(wind_rose)
    loader = DataLoader(database)
    exporter = await WeatherDatabase.export_to_xlsx(database)

    ui = UserInterface(database, exporter)
    # Запуск обновления погоды в отдельном таске
    asyncio.create_task(update_weather(extractor, transformer, loader))
    # Запуск интерфейса пользователя
    await ui.run()


async def update_weather(extractor, transformer, loader):
    while True:
        raw_data = await extractor.fetch_data()
        transformed_data = await transformer.transform_data(raw_data['current'], 'Москва')
        weather = Weather(**transformed_data)
        await loader.load_data(weather)
        delay = 0.1
        await asyncio.sleep(60 * delay) # Обновлять погоду каждые delay минут


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВнимание! Выполнение прервано пользователем.")
