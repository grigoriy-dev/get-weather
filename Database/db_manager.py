"""
Модуль для управления базой данных.

Этот модуль содержит класс DataBaseManager, который реализует функциональность для работы с базой данных,
включая сохранение, получение и экспорт данных.
"""

import pandas as pd
from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from contextlib import contextmanager

from .base import WeatherData, Weather, Base
from Interface.messages import success_message, error_message
from Settings.config import xlsx_path, db_path, rows, sqlite_database


class DataBaseManager:
    '''
    Класс-менеджер для управления данными в контексте БД.
    Используется @contextmanager для безопасных сессий.
    '''
    def __init__(self, sqlite_database):
        """
        Конструктор класса.
        Создает движок SQLAlchemy и инициализирует таблицы в базе данных.
        :param sqlite_database: Путь к базе данных SQLite.
        """
        self.engine = create_engine(sqlite_database, echo=False)
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Контекстный менеджер для управления сессией базы данных.
        Открывает новую сессию, фиксирует изменения и закрывает сессию.
        При возникновении ошибок откатывает транзакции.
        """
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()  # Откатываем изменения в случае ошибки
            raise e
        finally:
            session.close()

    async def save_weather(self, weather: Weather):
        # Сохраняет данные о погоде в базу данных.
        msg = 'Сохранение данных в БД'
        try:
            with self.session_scope() as session:
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
                session.add(new_record)
            print(success_message(msg))
        except Exception as e:
            print(error_message(msg, e))

    async def get_last_weather(self):
        # Возвращает последнюю запись о погоде из базы данных.
        with self.session_scope() as session:
            weather_data = session.query(WeatherData).order_by(WeatherData.id.desc()).first()
            
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
        # Экспортирует данные из базы данных в файл формата XLSX.
        msg = 'Экспорт данных в xlsx'
        try:
            with self.session_scope() as session:
                query = (
                        session.query(WeatherData)
                        .order_by(WeatherData.id.desc())
                        .limit(rows)
                )
                df = pd.read_sql_query(
                        query.statement, con=self.engine
                )
                with pd.ExcelWriter(xlsx_path, mode='w') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet_1')
                print(success_message(msg))
        except Exception as e:
            print(error_message(msg, e))
