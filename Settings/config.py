# Путь к базе данных
db_path = '/content/drive/My Drive/ColabNotebooks/gwth/files/weather_db.db'
# Путь к файлу .xlsx
xlsx_path = '/content/drive/My Drive/ColabNotebooks/gwth/files/weather.xlsx'

# Инициализация розы ветров
rose = range(0, 361, 45)
wind = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ', 'С']
wind_rose = dict(zip(rose, wind))

# Словарь, который содержит различные типы осадков
precipitation_map = {
    'rain': ('Дождь', 'rain'),
    'showers': ('Ливень', 'showers'),
    'snowfall': ('Снегопад', 'snowfall')
}

# Интервал получения данных о погоде (в минутах)
delay = 1

# ИНТЕРФЕЙС
def export_data(): pass
def show_data(): pass
# Доступные пользователю команды
command_dict = {
            '/export': export_data,
            '/show': show_data
        }
# Сообщение с доступными командами
help_message = (
            '\n---------- Доступные команды ----------'
            '\n/show - Вывести данные на экран'
            '\n/export - Экспортировать данные в .xlsx'
            '\n---------------------------------------'
        )

