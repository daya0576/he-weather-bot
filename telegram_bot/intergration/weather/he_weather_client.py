import asyncio
import random
from typing import Dict, List

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.intergration.weather.models.he_weather_model import HeWeatherModel
from telegram_bot.settings import aio_lru_cache_1h
from telegram_bot.util.date_util import DateUtil

WEATHER_MESSAGE_TEMPLATE = """
{Location}今天白天{d1_pretty}
明天{d2}，白天{d2_pretty}

{extra}
"""


class HeWeatherClient(WeatherClient):
    """ 和风天气客户端 """

    # 和风生活指数选项，随机选择
    LIFE_OPTIONS = tuple(range(1, 17))

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

    @aio_lru_cache_1h
    async def get_weather_forecast(self, location: Location) -> str:
        weather_3d_data, forecast_air, life_1d, warning = await asyncio.gather(
            self.get_weather_3d(location),
            self.get_air_now(location),
            self.get_indices_1d(location, random.choice(self.LIFE_OPTIONS)),
            self.get_warning_now(location),
        )
        d1_forecast_dict, d2_forecast_dict, _ = weather_3d_data

        # 构建天气预报数据模型
        d1_forecast = HeWeatherModel.build(d1_forecast_dict, air_now=forecast_air, warning=warning, indices=life_1d)
        d2_forecast = HeWeatherModel.build(d2_forecast_dict)

        # 组装最终天气文案
        extra = ""
        if d1_forecast.warning_text:
            extra = f"⚠️{d1_forecast.warning_text}"
        elif d1_forecast.life_text:
            extra = d1_forecast.life_text

        return WEATHER_MESSAGE_TEMPLATE.format(
            Location=location.name,
            d2=DateUtil.get_day(location.tz),
            d1_pretty=str(d1_forecast),
            d2_pretty=str(d2_forecast),
            extra=extra
        )

    async def get_weather_3d(self, location: Location) -> List:
        """城市天气API / 逐天天气预报"""
        result = await self._do_get("weather", "3d", {"location": location})
        return result.get("daily", [])

    async def get_indices_1d(self, location: Location, indices_type) -> List:
        """天气指数API / 天气生活指数"""
        params = {"location": location, "type": indices_type}
        result = await self._do_get("indices", "1d", params)
        return result.get("daily", [])

    async def get_air_now(self, location: Location) -> Dict:
        """空气API / 实时空气质量"""
        result = await self._do_get("air", "now", {"location": location})
        return result.get("now", {})

    async def get_warning_now(self, location: Location) -> Dict:
        """天气灾害预警"""
        result = await self._do_get("warning", "now", {"location": location})
        return result.get("warning", [])

    def get_weather_photo(self, location) -> str:
        pass
