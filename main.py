from Database.db_manager import DataBaseManager
import asyncio

async def main():
    mng = DataBaseManager
    extractor = mng.(latitude=55.751244, longitude=37.618423)
    transformer = DataTransformer(wind_rose)
    loader = DataLoader(database)
    exporter = DataExporter(database)
    ui = UserInterface(database, exporter)

    # Запуск обновления погоды в отдельном таске
    asyncio.create_task(update_weather(extractor, transformer, loader))

    # Запуск интерфейса пользователя
    await ui.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nВнимание! Выполнение прервано пользователем.")