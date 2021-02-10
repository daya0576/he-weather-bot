# -*- coding: utf-8 -*-

import requests
from aiogram import Bot
from requests.adapters import HTTPAdapter

from telegram_bot.intergration.weather.base_weather_client import WeatherClient

requests.adapters.DEFAULT_RETRIES = 3


class MessageService:
    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    async def send_weather_photo_to_chat(self, bot: Bot, chat_id: int):
        photo = self.weather_client.get_weather_photo()
        await bot.send_photo(chat_id=chat_id, photo=photo)

    async def send_weather_text_to_chat(self, bot: Bot, chat_id: int):
        text = self.weather_client.get_weather_forecast()
        await bot.send_message(chat_id=chat_id, text=text)
