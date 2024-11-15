"""
Модуль для определения моделей базы данных.

Этот модуль содержит определение базовых классов и моделей для работы с базой данных.
"""

from dataclasses import dataclass
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


@dataclass
class Weather:
    """
    Класс для представления данных о погоде.

    Атрибуты:
    - city (str): Название города.
    - date (str): Дата наблюдения.
    - time (str): Время наблюдения.
    - temperature (int): Температура воздуха.
    - wind_dir (str): Направление ветра.
    - wind_speed (int): Скорость ветра.
    - pressure (int): Атмосферное давление.
    - precipitation (str): Вид осадков.
    - prec_amount (int): Количество осадков.

    Используется декоратор @dataclass
    для автоматического создания методов __init__, __repr__ и других
    """
    city: str
    date: str
    time: str
    temperature: int
    wind_dir: str
    wind_speed: int
    pressure: int
    precipitation: str
    prec_amount: int


class Base(DeclarativeBase):
    """
    Абстрактный базовый класс для моделей базы данных.
    
    Методы __tablename__: 
    Автоматически генерирует имя таблицы на основе имени класса в нижнем регистре.
    """
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class WeatherData(Base):
    """
    Модель для хранения данных о погоде в базе данных.
    Наследует базовые свойства от класса Base.
    Содержит поля, соответствующие атрибутам класса Weather.
    """
    city: Mapped[str]
    date: Mapped[str]
    time: Mapped[str]
    temperature: Mapped[int]
    wind_dir: Mapped[str]
    wind_speed: Mapped[int]
    pressure: Mapped[int]
    precipitation: Mapped[str]
    prec_amount: Mapped[int]
