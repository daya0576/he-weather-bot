# -*- coding: utf-8 -*-
import os

import telegram

from telegram_bot.core.service.message import send_weather_forecast_to_channel

if __name__ == '__main__':
    bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))
    send_weather_forecast_to_channel(bot)
