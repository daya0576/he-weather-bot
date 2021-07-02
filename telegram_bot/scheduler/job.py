from urllib.parse import urljoin

import requests
from loguru import logger
from requests.adapters import HTTPAdapter, Retry

from telegram_bot.settings import settings


class CronJobsExecutor:

    @staticmethod
    def send_weather(user_id: str, user_cur_hour: str):
        with requests.Session() as s:
            retries = Retry(
                total=10,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504]
            )

            s.mount('http://', HTTPAdapter(max_retries=retries))
            s.mount('https://', HTTPAdapter(max_retries=retries))

            url = urljoin(settings.DOMAIN, "cron_send_weather_to_user")
            params = dict(user_id=user_id, user_cur_hour=user_cur_hour)

            logger.info(f"[http][get][request]{url},{params}")
            r = s.get(url, params=params)
            logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")
