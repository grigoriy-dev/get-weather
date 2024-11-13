from Database import base
import asyncio

async def main():
    # Инициализация объектов
    rose = range(0, 361, 45)
    wind = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ', 'С']
    wind_rose = dict(zip(rose, wind))

    database = WeatherDatabase(sqlite_database)
    extractor = DataExtractor(latitude=55.751244, longitude=37.618423)
    transformer = DataTransformer(wind_rose)
    loader = DataLoader(database)
    exporter = DataExporter(database)

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
        await asyncio.sleep(60 * delay)  # Обновлять погоду каждые delay минут


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВнимание! Выполнение прервано пользователем.")