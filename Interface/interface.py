from Database.db_manager import DataBaseManager as MNG

import asyncio


class UserInterface:
    def __init__(self, database: MNG):
        self.database = database
        self.command_dict = {
            '/show': self.show_data,
            '/export': self.export_data,
        }
        self.help_message = (
            '\n/show - Вывести данные на экран'
            '\n/export - Экспортировать данные в .xlsx'
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
        await self.database.export_to_xlsx()

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
