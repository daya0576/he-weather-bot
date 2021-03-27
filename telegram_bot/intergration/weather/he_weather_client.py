import asyncio
import random
from typing import Dict

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.intergration.weather.models.he_weather_model import HeWeatherModel
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
            # self._build_url("weather", "now", {"location": location}),
            self._build_url("weather", "3d", {"location": location}),
            self._build_url("indices", "1d", {"location": location, "type": random.choice(self.LIFE_OPTIONS)}),
            self._build_url("air", "5d", {"location": location})
        )
        tasks = [asyncio.create_task(self.http_client.get(url)) for url in urls]
        # TODO: pycharm warning
        # https://youtrack.jetbrains.com/issue/PY-47635
        forecast_data, life_data_now, forecast_air = await asyncio.gather(*tasks)

        # 天气预测 & 生活指数
        d1_forecast, d2_forecast, _ = forecast_data.get("daily")
        d1_air = self._get_latest_day(forecast_air)
        d1_life = self._get_latest_day(life_data_now)

        d1_life_pretty = d1_life.get("text", "")
        d1_pretty = HeWeatherModel.build(d1_forecast, air=d1_air)
        d2_pretty = HeWeatherModel.build(d2_forecast)

        # 组装最终结果
        return WEATHER_MESSAGE_TEMPLATE.format(
            Location=location.name,
            tomorrow=DateUtil.get_tomorrow_day(location.tz),
            d1_pretty=d1_pretty,
            d2_pretty=d2_pretty,
            life_pretty=d1_life_pretty
        )

    @staticmethod
    def _get_latest_day(data: Dict) -> dict:
        if not data:
            return {}

        data_list = data.get("daily")
        if not data_list:
            return {}

        return data_list[0]
