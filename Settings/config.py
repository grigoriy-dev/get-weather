"""
Конфигурационный файл проекта.

Этот модуль содержит пути к базам данных, словари данных и глобальные переменные.
"""

# Интервал получения данных о погоде (в минутах)
delay = 0.1
# Ограничение на количество строк для экспорта в файлы
rows = 10

# Путь к базе данных
db_path = '/content/drive/MyDrive/GitHub/get-weather/files/weather_db.db'

# Путь к файлу .xlsx для экспорта {rows}записей
xlsx_path = '/content/drive/MyDrive/GitHub/get-weather/files/weather.xlsx'

# Путь к файлу с городами и координатами, пример: {'Москва': (55.755825, 37.617298)}
cities_path = '/content/drive/MyDrive/GitHub/get-weather/files/cities.json'

# Конфигурация базы данных
sqlite_database = "sqlite:///" + db_path

# Инициализация розы ветров
rose = range(0, 361, 45)
wind = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ', 'С']
wind_rose = dict(zip(rose, wind))

# Словарь, который содержит различные типы осадков
precipitation_map = {
    'rain': ('Дождь', 'rain'),
    'showers': ('Ливень', 'showers'),
    'snowfall': ('Снегопад', 'snowfall')
}
