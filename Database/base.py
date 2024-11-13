from dataclasses import dataclass
from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from Settings.config import db_path


# Конфигурация базы данных
sqlite_database = "sqlite:///" + db_path
engine = create_engine(sqlite_database, echo=False)


@dataclass
class Weather:
    '''
    Использует декоратор @dataclass для автоматического создания методов __init__, __repr__ и других
    '''
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
    Базовый класс для моделей базы данных.
    Он является абстрактным, поэтому отдельная таблица для него не создается.
    Имя таблицы для каждой модели определяется именем класса в нижнем регистре.
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
    Содержит следующие поля:
    - city: название города
    - date: дата наблюдения
    - time: время наблюдения
    - temperature: температура воздуха
    - wind_dir: направление ветра
    - wind_speed: скорость ветра
    - pressure: атмосферное давление
    - precipitation: вид осадков
    - prec_amount: количество осадков
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
