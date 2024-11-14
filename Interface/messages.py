# Модуль предназначен для формирования сообщений.
from Settings.config import delay

CITY_TEMPLATE = 'Записываются данные о погоде в г.{} каждые {} минут(ы).'
SUCCESS_TEMPLATE = '{}: успешно.'
ERROR_TEMPLATE = 'Внимание! {}:'

def city_message(city):
    return CITY_TEMPLATE.format(city, delay)

def success_message(operation: str) -> str:
    # Успешное выполнение операции.
    return SUCCESS_TEMPLATE.format(operation)

def error_message(operation, error=None):
    message = ERROR_TEMPLATE.format(operation)
    if error:
        message += f': {error}.'
    return message
