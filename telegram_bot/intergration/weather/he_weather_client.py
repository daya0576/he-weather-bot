import asyncio
import random
from typing import Dict, List

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.intergration.weather.models.he_weather_model import HeWeatherModel
from telegram_bot.settings import aio_lru_cache
from telegram_bot.util.date_util import DateUtil

WEATHER_MESSAGE_TEMPLATE = """
{Location}今日{d1_pretty}

明日{d2}，白天{d2_pretty}
"""


class HeWeatherClient(WeatherClient):
    """ 和风天气客户端 """

    # 和风生活指数选项，随机选择
    LIFE_OPTIONS = (1, 3, 5, 6, 8, 9, 10, 15, 16)

    def __init__(self, http_client: HttpClient, key: str):
        self.http_client = http_client
        self.key = key

    async def _do_get(self, api_type, weather_type, params: Dict) -> Dict:
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}"
        params.update(key=self.key)
        response = await self.http_client.get(url, params)

        # API状态码校验，具体含义请参考：https://dev.qweather.com/docs/start/status-code/
        result_code = response.get("code")
        if result_code not in ("200", "204", "403"):
            raise Exception(f"qweather api returns code {result_code}!!")

        return response

    @aio_lru_cache
    async def get_weather_forecast(self, location: Location) -> str:
        weather_3d, forecast_air = await asyncio.gather(
            self.get_weather_3d(location),
            self.get_air_now(location),
        )
        d1_forecast, d2_forecast, _ = weather_3d

        return WEATHER_MESSAGE_TEMPLATE.format(
            Location=location.name,
            d2=DateUtil.get_day(location.tz),
            d1_pretty=HeWeatherModel.build(d1_forecast, air_now=forecast_air),
            d2_pretty=HeWeatherModel.build(d2_forecast),
        )

    async def get_weather_3d(self, location: Location) -> List:
        """城市天气API / 逐天天气预报"""
        result = await self._do_get("weather", "3d", {"location": location})
        return result.get("daily", [])

    async def get_indices_1d(self, location: Location) -> List:
        """天气指数API / 天气生活指数"""
        params = {"location": location, "type": random.choice(self.LIFE_OPTIONS)}
        result = await self._do_get("indices", "1d", params)
        return result.get("daily", [])

    async def get_air_now(self, location: Location) -> Dict:
        """空气API / 实时空气质量"""
        result = await self._do_get("air", "now", {"location": location})
        return result.get("now", {})

    def get_weather_photo(self, location) -> str:
        pass
