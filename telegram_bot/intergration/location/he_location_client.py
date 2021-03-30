from dataclasses import dataclass
from typing import Optional

from telegram_bot.intergration.http.base_http_client import HttpClient
from telegram_bot.settings import settings

KEY = settings.HE_WEATHER_API_TOKEN


@dataclass
class Location:
    name: str
    lat: float
    lon: float
    tz: str
    province: Optional[str] = ""
    country: Optional[str] = ""
    url: Optional[str] = ""

    def __eq__(self, o: "Location") -> bool:
        return self.lat == o.lat and self.lon == o.lon

    def __hash__(self) -> int:
        return hash((self.lat, self.lon))

    def __str__(self):
        city = f"{self.lon},{self.lat}" if self.lat and self.lon else self.name
        return city

    __repr__ = __str__


class HeLocationClient:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    URL = f"https://geoapi.qweather.com/v2/city/lookup?location={{}}&key={KEY}"

    async def _fetch(self, location) -> Optional[Location]:
        url = self.URL.format(location)
        d = await self.http_client.get(url)

        location_list = d.get("location")
        if not location_list:
            return

        d_location = location_list[0]
        return Location(
            name=d_location["name"],
            lat=float(d_location["lat"]),
            lon=float(d_location["lon"]),
            tz=d_location["tz"],
            province=d_location["adm1"],
            country=d_location["country"],
            url=d_location["fxLink"],
        )

    async def get_location_by_city_keywords(self, keywords) -> Optional[Location]:
        if not keywords:
            return
        return await self._fetch(keywords)

    async def get_location_by_lat_lon(self, lat, lon) -> Optional[Location]:
        if not (lat or lon):
            return
        return await self._fetch(f"{lon},{lat}")
