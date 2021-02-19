import random
from typing import Dict

from telegram_bot.intergration.http import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.settings import settings
from telegram_bot.util.date_util import DateUtil

KEY = settings.HE_WEATHER_API_TOKEN


class HeWeatherClient(WeatherClient):
    LIFE_OPTIONS = (1, 3, 5, 6, 8, 9, 10, 15, 16)

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def _fetch(self, api_type, weather_type, params: Dict):
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}?key={KEY}"
        for k, v in params.items():
            url += f"&{k}={v}"

        return self.http_client.get(url)

    def get_weather_photo(self, location) -> str:
        pass

    def get_weather_forecast(self, location: Location):
        # 天气预测：
        forecast_data = self._fetch("weather", "3d", {"location": location})
        weather_data = forecast_data.get("daily")
        d1 = weather_data[0]
        d1_pretty = self._format_weather_forecast(d1)
        d2 = weather_data[1]
        d2_pretty = self._format_weather_forecast(d2)

        # 生活指数
        life_data_d = self._fetch("indices", "1d", {"location": location, "type": random.choice(self.LIFE_OPTIONS)})
        life_pretty = self._format_life_weahter(life_data_d)

        return f"{location.name}今日{d1_pretty}。{life_pretty}\n\n" \
               f"明日{DateUtil.get_tomorrow_day()}，{d2_pretty}。"

    @staticmethod
    def _format_weather_forecast(d1):
        d1_n_str = d1['textDay']
        if d1['textNight'] != d1['textDay']:
            d1_n_str += f"，夜间{d1['textNight']}"

        return f"{d1_n_str}，{d1['tempMin']}到{d1['tempMax']}度"

    @staticmethod
    def _format_life_weahter(life_data: Dict):
        if "daily" in life_data:
            life_data_list = life_data["daily"]
            if life_data_list and 'text' in life_data_list[0]:
                return life_data_list[0]['text']

        return ""
