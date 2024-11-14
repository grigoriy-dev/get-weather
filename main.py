from Settings.config import cities, wind_rose, sqlite_database, delay
from Database.db_manager import DataBaseManager
from Tools.extractor import DataService
from Tools.upd_weather import update_weather
from Interface.interface import UserInterface as UI
import asyncio


async def main():
    city = "Москва"
    latitude, longitude = cities[city]

    print(f'Записываются данные о погоде в г.{city} каждые {delay} минут(ы).')

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


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВнимание! Выполнение прервано пользователем.")
