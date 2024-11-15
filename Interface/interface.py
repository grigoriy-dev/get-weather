"""
Модуль для реализации пользовательского интерфейса.

Этот модуль содержит класс UserInterface, который управляет взаимодействием с пользователем,
принимает команды и вызывает соответствующие методы для выполнения операций.
"""

import asyncio

from Database.db_manager import DataBaseManager as MNG
from .messages import help_message, show_me_weather


class UserInterface:
    """
    Класс для управления пользовательским интерфейсом.
    Этот класс обрабатывает ввод команд от пользователя и выполняет соответствующие действия.
    """
    def __init__(self, database: MNG):
        self.database = database
        self.command_dict = {
            '/show': self.show_data,
            '/export': self.export_data,
        }

    async def run(self):
        """
        Основной цикл обработки команд пользователя.

        Ожидает ввода команды от пользователя, проверяет ее наличие в словаре команд
        и вызывает соответствующую функцию. Если команда неизвестна, выводит сообщение помощи.
        """
        while True:
            try:
                cmd = await asyncio.get_event_loop().run_in_executor(None, input)
                if cmd in self.command_dict:
                    await self.command_dict[cmd]()
                    continue
                else:
                    print(help_message)
            except EOFError:
                break

    async def export_data(self):
        # Экспортирует данные о погоде в файл формата .xlsx.
        await self.database.export_to_xlsx()

    async def show_data(self):
        # Получает последние данные о погоде и выводит их на экран.
        last_weather = await self.database.get_last_weather()
        print(show_me_weather(last_weather))
