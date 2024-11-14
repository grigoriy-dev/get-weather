# Модуль предназначен для формирования сообщений.

SUCCESS_TEMPLATE = '{}: успешно.'
ERROR_TEMPLATE = 'Внимание! {}:'

def success_message(operation: str) -> str:
    # Успешное выполнение операции.
    return SUCCESS_TEMPLATE.format(operation)

def error_message(operation, error=None):
    message = ERROR_TEMPLATE.format(operation)
    if error:
        message += f': {error}.'
    return message
