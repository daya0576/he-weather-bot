import requests

from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.intergration.weather.base_weather_client import WeatherClient
from telegram_bot.settings import settings
from telegram_bot.util.date_util import DateUtil

KEY = settings.HE_WEATHER_API_TOKEN


class HeWeatherClient(WeatherClient):

    def _fetch(self, api_type, weather_type, location):
        url = f"https://devapi.qweather.com/v7/{api_type}/{weather_type}?location={location}&key={KEY}"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()

    def get_weather_photo(self, location) -> str:
        pass

    def get_weather_forecast(self, location: Location):
        city = f"{location.lon},{location.lat}" if location.lat and location.lon else location.name
        data = self._fetch("weather", "3d", city)
        weather_data = data.get("daily")

        # 天气预测：
        d1 = weather_data[0]
        d2 = weather_data[1]
        weather_data_today_str = f"{location.name}今日{self._format_weather(d1)}\n\n" \
                                 f"明日{DateUtil.get_tomorrow_day()}，{self._format_weather(d2)}"

        return weather_data_today_str

    def _format_weather(self, d1):
        d1_n_str = d1['textDay']
        if d1['textNight'] != d1['textDay']:
            d1_n_str += f"，夜间{d1['textNight']}"

        return f"{d1_n_str}，{d1['tempMin']}到{d1['tempMax']}度。"
