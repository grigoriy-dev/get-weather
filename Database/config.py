from sqlalchemy.orm import Session, DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine
import asyncio
import pandas as pd

# Путь к базе данных
db_path = 'files/weather_db.db'

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

    async def export_to_xlsx(self):
        rows = 10
        path = 'files/weather.xlsx'
        query = WeatherData.__table__.select().order_by(WeatherData.id.desc()).limit(rows)
        df = pd.read_sql_query(query, con=self.engine)
        with pd.ExcelWriter(path, mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet_1')
        print('Данные экспортированы\n')
