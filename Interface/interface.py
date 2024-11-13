import asyncio
from Database.config import WeatherDatabase, Weather, sqlite_database

# Путь к файлу .xlsx
xlsx_path = 'files/weather.xlsx'

# Класс инициализирует пользовательский интерфейс
class UserInterface:
    def __init__(self, database: WeatherDatabase, exporter: WeatherDatabase.export_to_xlsx):
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
