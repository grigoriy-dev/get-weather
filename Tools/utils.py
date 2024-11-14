import asyncio
from math import ceil, floor

from Settings.config import wind_rose


async def round_value(value):
    # математическое округление температуры
    if value % 1 >= 0.5:
        return ceil(value)
    else:
        return floor(value)

async def get_wind_direction(wind_grade):
    # извлечения направления ветра из розы ветров
    rose = wind_rose
    return rose[min(rose, key=lambda x: abs(x - wind_grade))]