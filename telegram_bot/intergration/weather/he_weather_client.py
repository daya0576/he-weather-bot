import asyncio
import random
from typing import Dict

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.settings import aio_lru_cache, settings
from telegram_bot.util.date_util import DateUtil

KEY = settings.HE_WEATHER_API_TOKEN

WEATHER_MESSAGE_TEMPLATE = """
{Location}今日{d1_pretty}
明日{tomorrow}，{d2_pretty}

{life_pretty}
"""


class HeWeatherClient(WeatherClient):
    """ 和风天气客户端 """

    # 和风生活指数选项，随机选择
    LIFE_OPTIONS = (1, 3, 5, 6, 8, 9, 10, 15, 16)
    ONE_HOUR = 60 * 60

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    @staticmethod
    def _build_url(api_type, weather_type, params: Dict) -> str:
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}?key={KEY}"
        for k, v in params.items():
            url += f"&{k}={v}"

        return url

    async def get_weather_photo(self, location) -> str:
        pass

    @aio_lru_cache
    async def get_weather_forecast(self, location: Location) -> str:
        urls = (
            self._build_url("weather", "now", {"location": location}),
            self._build_url("weather", "3d", {"location": location}),
            self._build_url("indices", "1d", {"location": location, "type": random.choice(self.LIFE_OPTIONS)})
        )
        tasks = [asyncio.create_task(self.http_client.get(url)) for url in urls]
        # TODO: pycharm warning
        # https://youtrack.jetbrains.com/issue/PY-47635
        weather_now, forecast_data, life_data_now = await asyncio.gather(*tasks)

        # 天气预测 & 生活指数
        d1, d2, _ = forecast_data.get("daily")
        d1_pretty = self._format_weather_forecast(d1, weather_now.get("now"))
        d2_pretty = self._format_weather_forecast(d2)
        life_pretty = self._format_life_weather(life_data_now)

        return WEATHER_MESSAGE_TEMPLATE.format(
            Location=location.name,
            d1_pretty=d1_pretty,
            tomorrow=DateUtil.get_tomorrow_day(location.tz),
            d2_pretty=d2_pretty,
            life_pretty=life_pretty
        )

    @staticmethod
    def _format_weather_forecast(d, d_now=None) -> str:
        if not d or 'textDay' not in d:
            return ""

        d_str = f"白天{d['textDay']}({d['tempMin']}°~{d['tempMax']}°)"

        if d_now and 'temp' in d_now:
            d_str += f"，当前气温{d_now['temp']}°C"

        if d['textNight'] != d['textDay']:
            d_str += f"，夜晚{d['textNight']}"

        return d_str

    @staticmethod
    def _format_life_weather(life_data: Dict) -> "":
        if not life_data:
            return ""

        if life_data_list := life_data.get("daily"):
            return life_data_list[0].get('text')

        return ""
