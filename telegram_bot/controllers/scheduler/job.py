from urllib.parse import urljoin

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from telegram_bot.settings import settings

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)


class CronTaskExecutor:
    def __init__(self):
        self.s = requests.Session()
        self.s.mount('http://', HTTPAdapter(max_retries=retries))
        self.s.mount('https://', HTTPAdapter(max_retries=retries))

    def send_weather(self, user_id: str, user_cur_hour: str):
        url = urljoin(settings.DOMAIN, "cron_send_weather_to_user")
        params = dict(user_id=user_id, user_cur_hour=user_cur_hour)

        logger.info(f"[http][get][request]{url},{params}")
        r = self.s.get(url, params=params)
        logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")

    def send_warning(self, user_id: str):
        url = urljoin(settings.DOMAIN, "cron_warning_to_user")
        params = dict(user_id=user_id)

        logger.info(f"[http][get][request]{url},{params}")
        r = self.s.get(url, params=params)
        logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")
