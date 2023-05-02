from typing import Dict, Optional

import httpx
from loguru import logger
from tenacity import retry, stop_after_attempt

from telegram_bot.intergration.http.base_http_client import HttpClient


class HttpxClient(HttpClient):
    def __init__(self):
        transport = httpx.AsyncHTTPTransport(retries=3)
        timeout = httpx.Timeout(15.0, connect=60.0)
        self.client = httpx.AsyncClient(transport=transport, timeout=timeout)

    @retry(stop=stop_after_attempt(3))
    async def get(self, url: str, params: Optional[Dict] = None) -> Dict:
        logger.info(f"[http][get][request]{url}")
        r = await self.client.get(url, params=params)
        logger.info(f"[http][get][response]{url},{r.status_code},{r.json()}")

        r.raise_for_status()
        return r.json()

    @retry(stop=stop_after_attempt(3))
    async def post(self, url: str, params: Optional[Dict] = None) -> Dict:
        logger.info(f"[http][post][request]{url}")
        headers = {"Content-Type": "application/json"}
        r = await self.client.post(url, json=params, headers=headers)
        logger.info(f"[http][post][response]{url},{r.status_code},{r.json()}")

        r.raise_for_status()
        return r.json()
