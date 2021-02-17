# -*- coding: utf-8 -*-

#
# def send_weather_forecast_to_channel(bot):
#     chat_ids = os.environ["CHAT_IDS"].split(',')
#     for chat_id in chat_ids:
#         send_weather_forecast(bot, chat_id)
from telegram_bot.intergration import he_weather
from telegram_bot.intergration.location.he_location_client import Location

if __name__ == '__main__':
    # bot = telegram.Bot(token=(os.environ['TELEGRAM_TOKEN']))
    # send_weather_forecast_to_channel(bot)

    location = Location(name="北京", lat=39.92, lon=116.41, tz="")
    print(he_weather.get_weather_forecast(location))
