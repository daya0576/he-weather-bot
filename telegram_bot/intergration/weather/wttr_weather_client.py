import requests

from telegram_bot.intergration.weather.base_weather_client import WeatherClient


class AsciiWeatherClient(WeatherClient):
    def get_weather_photo(self, location) -> str:
        return f"wttr.in/31.23,121.47.png?2nFqQ"

    def get_weather_forecast(self, location) -> str:
        return requests.get(f"http://wttr.in/shanghai").text
