from Settings.config import command_dict, help_message

import asyncio


class UserInterface:
    def __init__(self, database: WeatherDatabase, exporter: DataExporter):
        self.database = database
        self.exporter = exporter
        self.command_dict = command_dict
        self.help_message = help_message

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
        await self.exporter.export_to_xlsx()

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
