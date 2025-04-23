import asyncio
import random
from typing import Dict, List, Optional
from urllib.parse import urljoin

from loguru import logger

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.intergration.weather.const import (
    WEATHER_2D_MESSAGE_TEMPLATE,
    WEATHER_6H_MESSAGE_TEMPLATE,
)
from telegram_bot.intergration.weather.models.he_weather_model import HeWeatherModel
from telegram_bot.intergration.weather.models.warn_model import WarnModel
from telegram_bot.settings import aio_lru_cache_1h
from telegram_bot.utils.date_util import DateUtil


class HeWeatherClient(WeatherClient):
    """和风天气客户端"""

    # 和风生活指数选项，随机选择
    LIFE_OPTIONS = tuple(range(1, 17))

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    #################################### 对外接口 ####################################
    @aio_lru_cache_1h
    async def get_weather_forecast(self, location: Location) -> str:
        weather_3d_data, forecast_air, life_1d = await asyncio.gather(
            self._get_weather_3d(location),
            self._get_air_now(location),
            self._get_indices_1d(location, random.choice(self.LIFE_OPTIONS)),
        )
        d1_forecast_dict, d2_forecast_dict = weather_3d_data[:2]

        # 构建天气预报数据模型
        d1_forecast = HeWeatherModel.build(
            d1_forecast_dict, air_now=forecast_air, indices=life_1d
        )
        d2_forecast = HeWeatherModel.build(d2_forecast_dict)

        # 组装最终天气文案
        extra = ""
        if d1_forecast.warning_text:
            extra = f"⚠️{d1_forecast.warning_text}"
        elif d1_forecast.life_text:
            extra = d1_forecast.life_text

        return WEATHER_2D_MESSAGE_TEMPLATE.format(
            location=location.name,
            d1=DateUtil.get_day_of_week(location.tz, 0),
            d2=DateUtil.get_day_of_week(location.tz, 1),
            d1_pretty=str(d1_forecast),
            d2_pretty=str(d2_forecast),
            extra=extra,
        )

    async def get_weather_warning(self, location: Location) -> Optional[WarnModel]:
        """获取自然灾害信息"""
        warning_list = await self._get_warning_now(location)
        if not warning_list:
            return

        w = warning_list[0]
        return WarnModel(w["text"], w["typeName"], w["level"])

    async def get_weather_6h_forecast_text(self, location: Location) -> str:
        d = await self._get_weather_hour(location)
        hour = DateUtil.get_cur_hour(location.tz)
        hours_text = "\n".join(
            f"{(hour + i) % 24:02d}:00：{d[i]['text']} {d[i]['temp']}℃"
            for i in range(6)
        )

        return WEATHER_6H_MESSAGE_TEMPLATE.format(
            location=location.name, hours=hours_text
        )

    #################################### 原始接口 ####################################
    async def _do_get(
        self, api_type, weather_type, location: Location, params: Dict = None
    ) -> Dict:
        assert location.key and location.host
        endpoint, key = f"https://{location.host}", location.key
        url = urljoin(endpoint, f"/v7/{api_type}/{weather_type}")

        params = params or {}
        params["location"] = location.get_location()

        headers = {"X-QW-Api-Key": key}
        logger.warning(headers)

        return await self.http_client.get(url, params, headers=headers)

    async def _get_weather_3d(self, location: Location) -> List:
        """城市天气API / 逐天天气预报"""
        result = await self._do_get("weather", "3d", location)
        return result.get("daily", [])

    async def _get_weather_hour(self, location: Location) -> List:
        """城市天气API / 逐小时天气预报"""
        result = await self._do_get("weather", "24h", location)
        return result.get("hourly", [])

    async def _get_indices_1d(self, location: Location, indices_type) -> List:
        """天气指数API / 天气生活指数"""
        params = {"type": indices_type}
        result = await self._do_get("indices", "1d", location, params)
        return result.get("daily", [])

    async def _get_air_now(self, location: Location) -> Dict:
        """空气API / 实时空气质量"""
        result = await self._do_get("air", "now", location)
        return result.get("now", {})

    async def _get_warning_now(self, location: Location) -> List[Dict]:
        """天气灾害预警"""
        result = await self._do_get("warning", "now", self._build_params(location))
        return result.get("warning", [])

    def get_weather_photo(self, location) -> str: ...
