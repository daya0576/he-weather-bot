from abc import ABC, abstractmethod


class WeatherClient(ABC):
    @abstractmethod
    def get_weather_forecast(self) -> str:
        pass

    @abstractmethod
    def get_weather_photo(self) -> str:
        pass
