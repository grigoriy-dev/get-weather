import asyncio
from math import ceil, floor

# Класс для преобразования сырых данных
class DataTransformer:
    def __init__(self, rose):
        self.rose = rose

    async def round_value(self, value):
        # математическое округление температуры
        if value % 1 >= 0.5:
            return ceil(value)
        else:
            return floor(value)

    async def get_wind_direction(self, wind_grade):
        # извлечения направления ветра из розы ветров
        return self.rose[min(self.rose, key=lambda x: abs(x - wind_grade))]

    async def transform_data(self, raw_data, city):
        # преобразование данных
        transformed_data = {
            'city': city,
            'date': raw_data['time'][:10],
            'time': raw_data['time'][11:],
            'temperature': await self.round_value(raw_data['temperature_2m']),
            'wind_dir': await self.get_wind_direction(raw_data['wind_direction_10m']),
            'wind_speed': await self.round_value(raw_data['wind_speed_10m']),
            'pressure': await self.round_value(raw_data['surface_pressure'])
        }

        # Cловарь, который содержит различные типы осадков
        precipitation_map = {
            'rain': ('Дождь', 'rain'),
            'showers': ('Ливень', 'showers'),
            'snowfall': ('Снегопад', 'snowfall')
        }

        for key, (prec_type, amount_key) in precipitation_map.items():
            if key in raw_data:
                transformed_data['precipitation'] = prec_type
                transformed_data['prec_amount'] = raw_data[amount_key]
                break
        else:
            transformed_data['precipitation'] = 'Без осадков'
            transformed_data['prec_amount'] = 0

        return transformed_data
