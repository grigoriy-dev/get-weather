import csv
import asyncio
import aiohttp
import pandas as pd
from typing import Any
from math import ceil, floor
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session, DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine
# В Colaboratory Google по умолчанию уже запущен цикл событий


# Путь к базе данных
db_path = '/files/weather_db.db'
# Путь к файлу .xlsx
xlsx_path = '/files/weather.xlsx'

# Конфигурация базы данных
sqlite_database = "sqlite:///" + db_path
engine = create_engine(sqlite_database, echo=False)

# Класс, представляющий собой набор данных о погоде в конкретный момент времени
class Weather:
    def __init__(self, city, date, time, temperature, wind_dir, wind_speed, pressure, precipitation, prec_amount):
        self.city = city
        self.date = date
        self.time = time
        self.temperature = temperature
        self.wind_dir = wind_dir
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.precipitation = precipitation
        self.prec_amount = prec_amount

class Base(DeclarativeBase):
    # Класс абстрактный, чтобы не создавать отдельную таблицу для него
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class WeatherData(Base):
    city: Mapped[str]
    date: Mapped[str]
    time: Mapped[str]
    temperature: Mapped[int]
    wind_dir: Mapped[str]
    wind_speed: Mapped[int]
    pressure: Mapped[int]
    precipitation: Mapped[str]
    prec_amount: Mapped[int]

# Класс-Менеджер взаимодействия с базой данных
class WeatherDatabase:
    def __init__(self, sqlite_database):
        self.engine = create_engine(sqlite_database, echo=False)
        Base.metadata.create_all(self.engine)

    async def save_weather(self, weather: Weather):
        with Session(bind=self.engine) as db:
            new_record = WeatherData(
                city=weather.city,
                date=weather.date,
                time=weather.time,
                temperature=weather.temperature,
                wind_dir=weather.wind_dir,
                wind_speed=weather.wind_speed,
                pressure=weather.pressure,
                precipitation=weather.precipitation,
                prec_amount=weather.prec_amount
            )
            db.add(new_record)
            db.commit()
        print('Данные успешно сохранены в БД')

    async def get_last_weather(self):
        # извлечение последней записи из БД
        with Session(bind=self.engine) as db:
            weather_data = db.query(WeatherData).order_by(WeatherData.id.desc()).first()
            if weather_data:
                return Weather(
                    city=weather_data.city,
                    date=weather_data.date,
                    time=weather_data.time,
                    temperature=weather_data.temperature,
                    wind_dir=weather_data.wind_dir,
                    wind_speed=weather_data.wind_speed,
                    pressure=weather_data.pressure,
                    precipitation=weather_data.precipitation,
                    prec_amount=weather_data.prec_amount
                )
            else:
                raise ValueError("No weather data available.")

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

# Класс загрузчик данных, сохраняет данные в базу данных
class DataLoader:
    def __init__(self, database: WeatherDatabase):
        self.database = database

    async def load_data(self, weather: Weather):
        await self.database.save_weather(weather)

# Класс экспортирует данные в Excel-файл
class DataExporter:
    def __init__(self, database):
        self.database = database

    async def export_to_xlsx(self, path, rows=10):
        query = WeatherData.__table__.select().order_by(WeatherData.id.desc()).limit(rows)
        df = pd.read_sql_query(query, con=self.database.engine)
        with pd.ExcelWriter(path, mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet_1')
        print('Данные экспортированы\n')

# Класс инициализирует пользовательский интерфейс
class UserInterface:
    def __init__(self, database: WeatherDatabase, exporter: DataExporter):
        self.database = database
        self.exporter = exporter
        self.command_dict = {
            '/export': self.export_data,
            '/show': self.show_data
        }
        self.help_message = (
            '\n--- Доступные команды: ---'
            '\n/show - Вывести данные на экран'
            '\n/export - Экспортировать данные в .xlsx'
            '\n---------------------------'
        )

    async def run(self):
        # функция принимает команды от пользователя
        while True:
            try:
                cmd = await asyncio.get_event_loop().run_in_executor(None, input)
                if cmd in self.command_dict:
                    await self.command_dict[cmd]()
                    continue
                else:
                    print(self.help_message)
            except EOFError:
                break

    async def export_data(self):
        await self.exporter.export_to_xlsx(xlsx_path)

    async def show_data(self):
        last_weather = await self.database.get_last_weather()
        print(f'''
Погода в Москве на {last_weather.date} в {last_weather.time}:
Температура: {last_weather.temperature}*C
Направление ветра: {last_weather.wind_dir}
Скорость ветра: {last_weather.wind_speed} м/с
Давление: {last_weather.pressure} мм рт. ст.
Осадки: {last_weather.precipitation}, {last_weather.prec_amount} мм
''')


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
