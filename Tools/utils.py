async def round_value(self, value):
    # математическое округление температуры
    if value % 1 >= 0.5:
        return ceil(value)
    else:
        return floor(value)

async def get_wind_direction(self, wind_grade):
    # извлечения направления ветра из розы ветров
    return self.rose[min(self.rose, key=lambda x: abs(x - wind_grade))]