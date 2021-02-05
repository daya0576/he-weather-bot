# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter

requests.adapters.DEFAULT_RETRIES = 5


class Weather:
    def __init__(self, weather_client):
        self.client = weather_client

    def get_weather_forecast(self):
        return self.client.get_forecast_weather()
