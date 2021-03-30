from telegram_bot.intergration.http.httpx_client import HttpxClient
from telegram_bot.intergration.http.request_http_client import RequestHttpClient
from telegram_bot.intergration.location.he_location_client import HeLocationClient
from telegram_bot.intergration.weather.he_weather_client import HeWeatherClient
from telegram_bot.intergration.weather.wttr_weather_client import AsciiWeatherClient

# HTTP 客户端
from telegram_bot.settings import settings

request_cli = RequestHttpClient()
httpx_cli = HttpxClient()

# 和风天气预报客户端
he_weather = HeWeatherClient(httpx_cli, settings.HE_WEATHER_API_TOKEN)
ascii_weather = AsciiWeatherClient()
he_location_client = HeLocationClient(httpx_cli)

__all__ = [
    "he_weather",
    "ascii_weather",
    "he_location_client"
]
