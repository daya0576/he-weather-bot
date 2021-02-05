# -*- coding: utf-8 -*-

from telegram_bot.common.intergration import ascii_weather


def send_weather_forecast(bot, chat_id: str):
    bot.send_photo(chat_id=chat_id, photo=ascii_weather.get_weather_forecast())
