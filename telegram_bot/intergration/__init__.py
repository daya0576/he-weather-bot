from telegram_bot.intergration.dingding.dingbot import DingBotClient
from telegram_bot.intergration.http.httpx_client import HttpxClient
from telegram_bot.intergration.http.request_http_client import RequestHttpClient
from telegram_bot.intergration.location.he_location_client import HeLocationClient
from telegram_bot.intergration.weather.he_weather_client import HeWeatherClient
from telegram_bot.intergration.weather.wttr_weather_client import AsciiWeatherClient

request_cli = RequestHttpClient()
httpx_cli = HttpxClient()

# 和风天气预报客户端
he_weather = HeWeatherClient(httpx_cli)
ascii_weather = AsciiWeatherClient()
he_location_client = HeLocationClient(httpx_cli)

# 钉钉客户端
ding_bot_client = DingBotClient(httpx_cli)

__all__ = ["he_weather", "ascii_weather", "he_location_client", "ding_bot_client"]
