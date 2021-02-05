import requests

from telegram_bot.core.service.utils import get_tomorrow_day
from telegram_bot.intergration.base_weather_client import WeatherClient

KEY = "10857fb2911441269e7c60e26b269adb"


class HeWeatherClient(WeatherClient):
    def get_weather_forecast(self):
        pass

    def _fetch(self, api_type, weather_type):
        location = "shanghai"
        url = f"https://free-api.heweather.net/s6/{api_type}/{weather_type}?location={location}&key={KEY}"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()

    def _format_weather(self, d1):
        d1_n_str = ""
        if d1['cond_txt_n'] != d1['cond_txt_d']:
            d1_n_str = f"，夜间{d1['cond_txt_n']}"

        return f"{d1['cond_txt_d']}{d1_n_str}，{d1['tmp_min']}到{d1['tmp_max']}度。"

    def get_forecast_weather(self):
        data = self._fetch("weather", "forecast")
        weather_data = data.get("HeWeather6", {})[0].get("daily_forecast")

        # 天气预测：
        d1 = weather_data[0]
        d2 = weather_data[1]

        weather_data_today_str = f"上海今日{self._format_weather(d1)}\n\n" \
                                 f"明日{get_tomorrow_day()}，{self._format_weather(d2)}"

        return weather_data_today_str
