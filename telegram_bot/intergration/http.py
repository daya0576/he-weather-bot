from typing import Dict, List

from loguru import logger
from requests_futures.sessions import FuturesSession


class HttpClient:
    def __init__(self):
        self.session = FuturesSession()

    def post(self, url):
        pass

    def get(self, url) -> Dict:
        logger.info(f"[http][get][request],{url}")
        r = self.session.get(url).result()
        logger.info(f"[http][get][response],{r.status_code},{r.json()}")
        if r.status_code == 200:
            return r.json()

    def get_responses(self, urls: List[str]):
        for url in urls:
            logger.info(f"[http][get][request],{url}")
        futures = [self.session.get(url) for url in urls]

        responses = []
        for f in futures:
            r = f.result()
            logger.info(f"[http][get][response],{r.status_code},{r.json()}")
            if r.status_code == 200:
                responses.append(r.json())

        return responses
