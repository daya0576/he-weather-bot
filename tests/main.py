# -*- coding: utf-8 -*-
import os

import telegram

#
# def send_weather_forecast_to_channel(bot):
#     chat_ids = os.environ["CHAT_IDS"].split(',')
#     for chat_id in chat_ids:
#         send_weather_forecast(bot, chat_id)


if __name__ == '__main__':
    bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))
    # send_weather_forecast_to_channel(bot)
