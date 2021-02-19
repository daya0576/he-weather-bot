from typing import Dict

import requests
from fastapi.logger import logger


class HttpClient:
    def post(self, url):
        pass

    def get(self, url) -> Dict:
        logger.info(f"[http][get][request],{url}")
        r = requests.get(url)
        logger.info(f"[http][get][response],{r.status_code},{r.json()}")
        if r.status_code == 200:
            return r.json()
