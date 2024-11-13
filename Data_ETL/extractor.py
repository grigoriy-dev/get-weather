import aiohttp
import asyncio

# Класс, ответственный за извлечение данных из API
class DataExtractor:
    def __init__(self, latitude, longitude):
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "rain", "showers",
                "snowfall",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m"
            ],
            "timezone": "Europe/Moscow",
            "wind_speed_unit": "ms",
            "forecast_days": 1
        }

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed. Status code: {response.status}")