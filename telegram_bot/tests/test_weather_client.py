# -*- coding: utf-8 -*-
import asyncio

from telegram_bot.intergration import he_weather
from telegram_bot.intergration.location.he_location_client import Location
from telegram_bot.service.message import TelegramMessageService
from telegram_bot.telegram.dispatcher import dp


def test_beijin_weather():
    location = Location(name="北京", lat=39.92, lon=116.41, tz="")
    model = asyncio.run(he_weather.get_weather_warning(location))

    print(model)


def test_bot_blocked():
    asyncio.run(TelegramMessageService.send_text(dp.bot, "535189255", "text"))
