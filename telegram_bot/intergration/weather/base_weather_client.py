from abc import ABC, abstractmethod


class WeatherClient(ABC):
    @abstractmethod
    def get_weather_forecast(self, location) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_weather_photo(self, location) -> str:
        raise NotImplementedError
