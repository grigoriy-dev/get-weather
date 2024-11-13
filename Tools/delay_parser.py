

async def update_weather(extractor, transformer, loader):
    while True:
        raw_data = await extractor.fetch_data()
        transformed_data = await transformer.transform_data(raw_data['current'], 'Москва')
        weather = Weather(**transformed_data)
        await loader.load_data(weather)
        delay = 0.1
        await asyncio.sleep(60 * delay)  # Обновлять погоду каждые delay минут