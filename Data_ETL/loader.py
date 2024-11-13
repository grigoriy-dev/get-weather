import asyncio
from Database.config import WeatherDatabase, Weather

# Класс загрузчик данных, сохраняет данные в базу данных
class DataLoader:
    def __init__(self, database: WeatherDatabase):
        self.database = database

    async def load_data(self, weather: Weather):
        await self.database.save_weather(weather)