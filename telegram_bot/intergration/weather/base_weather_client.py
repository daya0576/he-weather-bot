from abc import ABC, abstractmethod


class WeatherClient(ABC):
    @abstractmethod
    def get_weather_forecast(self, location) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_weather_photo(self, location) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    __repr__ = __str__
