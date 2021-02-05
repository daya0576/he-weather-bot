from datetime import datetime

import pytz

from telegram_bot.common.intergration.base_weather_client import WeatherClient


class WttrWeatherClient(WeatherClient):
    def get_weather_forecast(self) -> str:
        tz = pytz.timezone('Asia/Shanghai')
        return f"wttr.in/31.23,121.47?2FnM&lang=zh-cn&{datetime.now(tz).timestamp()}"
