# -*- coding: utf-8 -*-

from telegram_bot.intergration import he_weather
from telegram_bot.intergration.location.he_location_client import Location


def test_beijin_weather():
    location = Location(name="北京", lat=39.92, lon=116.41, tz="")
    print(he_weather.get_weather_forecast(location))
