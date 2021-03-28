from urllib.parse import urljoin

import requests

from telegram_bot.settings import settings


def send_weather(user_id: str, user_cur_hour: str):
    requests.get(urljoin(settings.DOMAIN, "cron_send_weather_to_user"),
                 {"user_id": user_id, "user_cur_hour": user_cur_hour})
