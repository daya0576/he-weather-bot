from typing import Dict

from telegram_bot.intergration import HttpClient
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.settings import settings
from telegram_bot.util.date_util import DateUtil

KEY = settings.HE_WEATHER_API_TOKEN


class HeWeatherClient(WeatherClient):
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def _fetch(self, api_type, weather_type, params: Dict):
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}?key={KEY}"
        for k, v in params.items():
            url += f"&{k}={v}"

        r = self.http_client.get(url)
        if r.status_code == 200:
            return r.json()

    def get_weather_photo(self, location) -> str:
        pass

    def get_weather_forecast(self, location: Location):
        # 天气预测：
        forecast_data = self._fetch("weather", "3d", {"location": location})
        weather_data = forecast_data.get("daily")
        d1 = weather_data[0]
        d2 = weather_data[1]

        # 生活指数
        life_data = self._fetch("indices", "1d", {"location": location, "type": 8})
        life_d1 = life_data["daily"][0]['text']

        return f"{location.name}今日{self._format_weather(d1)}。{life_d1}\n\n" \
               f"明日{DateUtil.get_tomorrow_day()}，{self._format_weather(d2)}。"

    def _format_weather(self, d1):
        d1_n_str = d1['textDay']
        if d1['textNight'] != d1['textDay']:
            d1_n_str += f"，夜间{d1['textNight']}"

        return f"{d1_n_str}，{d1['tempMin']}到{d1['tempMax']}度"
