from abc import ABC, abstractmethod
from typing import Dict


class HttpClient(ABC):
    @abstractmethod
    async def get(self, url: str, params: Dict = None, headers: Dict = None) -> Dict:
        pass

    @abstractmethod
    async def post(self, url: str, params: Dict = None, headers: Dict = None) -> Dict:
        pass
