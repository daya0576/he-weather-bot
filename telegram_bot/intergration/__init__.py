from telegram_bot.intergration.http import HttpClient
from telegram_bot.intergration.location.he_location_client import HeLocationClient
from telegram_bot.intergration.weather.he_weather_client import HeWeatherClient
from telegram_bot.intergration.weather.wttr_weather_client import AsciiWeatherClient

http_cli = HttpClient()

he_weather = HeWeatherClient()
ascii_weather = AsciiWeatherClient()
he_location_client = HeLocationClient(http_cli)

__all__ = [
    "he_weather",
    "ascii_weather",
    "he_location_client"
]
