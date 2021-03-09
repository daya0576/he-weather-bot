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

    def _url(self, api_type, weather_type, params: Dict) -> str:
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}?key={KEY}"
        for k, v in params.items():
            url += f"&{k}={v}"

        return url

    async def get_weather_photo(self, location) -> str:
        pass

    def get_weather_forecast(self, location: Location):
        urls = [
            self._url("weather", "now", {"location": location}),
            self._url("weather", "3d", {"location": location}),
            self._url("indices", "1d", {"location": location, "type": random.choice(self.LIFE_OPTIONS)})
        ]
        weather_now, forecast_data, life_data_now = self.http_client.get_responses(urls)

        # 天气预测：
        d1, d2, _ = forecast_data.get("daily")
        d1_pretty = self._format_weather_forecast(d1, weather_now.get("now"))
        d2_pretty = self._format_weather_forecast(d2)
        # 生活指数
        life_pretty = self._format_life_weather(life_data_now)

        return f"{location.name}" \
               f"今天{d1_pretty}。\n" \
               f"明日{DateUtil.get_tomorrow_day()}，{d2_pretty}。\n" \
               f"\n" \
               f"{life_pretty}"

    @staticmethod
    def _format_weather_forecast(d, d_now=None) -> str:
        if not d or 'textDay' not in d:
            return ""

        d_str = f"白天{d['textDay']}（{d['tempMin']}°~{d['tempMax']}°）"

        if d_now and 'temp' in d_now:
            d_str += f"，当前气温{d_now['temp']}°"
        if d['textNight'] != d['textDay']:
            d_str += f"，夜晚{d['textNight']}"

        return d_str

    @staticmethod
    def _format_life_weather(life_data: Dict) -> "":
        if life_data and "daily" in life_data:
            life_data_list = life_data["daily"]
            if life_data_list and 'text' in life_data_list[0]:
                return life_data_list[0]['text']

        return ""
