# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter

from telegram_bot.intergration import he_weather

requests.adapters.DEFAULT_RETRIES = 5


class Weather:
    def __init__(self, weather_client):
        self.client = he_weather

    def format_weather(self, d1):
        d1_n_str = ""
        if d1['cond_txt_n'] != d1['cond_txt_d']:
            d1_n_str = f"，夜间{d1['cond_txt_n']}"

        return f"{d1['cond_txt_d']}{d1_n_str}，{d1['tmp_min']}到{d1['tmp_max']}度。"

    def get_weather(self):
        return self.client.get_forecast_weather()
