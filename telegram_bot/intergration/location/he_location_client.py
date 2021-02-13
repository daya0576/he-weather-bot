from dataclasses import dataclass
from typing import Optional

from telegram_bot.intergration.http import HttpClient
from telegram_bot.settings import settings

KEY = settings.HE_WEATHER_API_TOKEN


@dataclass
class Location:
    name: str
    lat: float
    lon: float
    tz: str


class HeLocationClient:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    URL = f"https://geoapi.qweather.com/v2/city/lookup?location={{}}&key={KEY}"

    def _fetch(self, location) -> Optional[Location]:
        url = self.URL.format(location)
        d = self.http_client.get(url)

        location_list = d.get("location")
        if not location_list:
            return

        d_location = location_list[0]
        return Location(
            name=d_location["name"],
            lat=float(d_location["lat"]),
            lon=float(d_location["lon"]),
            tz=d_location["tz"]
        )

    def get_location_by_city_keywords(self, keywords) -> Optional[Location]:
        if not keywords:
            return
        return self._fetch(keywords)

    def get_location_by_lat_lon(self, lat, lon) -> Optional[Location]:
        if not (lat or lon):
            return
        return self._fetch(f"{lon},{lat}")
