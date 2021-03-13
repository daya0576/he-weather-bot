from abc import ABC, abstractmethod
from typing import Dict


class HttpClient(ABC):
    @abstractmethod
    async def get(self, url: str, params: Dict = None) -> Dict:
        pass
