from typing import Dict

import httpx
from loguru import logger

from telegram_bot.intergration.http.base_http_client import HttpClient


class HttpxClient(HttpClient):

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get(self, url: str, params: Dict = None) -> Dict:
        """
        异步请求外部资源
        """
        logger.info(f"[http][get][request]{url}")
        r = await self.client.get(url, params=params)
        logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")

        if r.status_code == 200:
            return r.json()

        return {}
