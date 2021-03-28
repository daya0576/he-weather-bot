from dataclasses import dataclass
from typing import Dict

EMOJI_MAP = {
    "晴": "☀️",
    "晴间多云": "🌤",
    "雷阵雨": "⛈",
}


@dataclass
class HeWeatherModel:
    w_day: str
    w_night: str

    temp_min: str
    temp_max: str
    temp_now: str

    air_aqi: str
    air_text: str

    @classmethod
    def build(cls, day: Dict, now: Dict = None, air: Dict = None):
        now = now or {}
        air = air or {}
        return cls(
            day.get("textDay"),
            day.get("textNight"),
            day.get("tempMin"),
            day.get("tempMax"),
            now.get("temp"),
            air.get("aqi"),
            air.get("category"),
        )

    @property
    def w_day_emoji(self):
        if emoji := EMOJI_MAP.get(self.w_day):
            return emoji

        if "雪" in self.w_day:
            return "❄️"
        if "雨" in self.w_day:
            return "🌧"
        if "云" in self.w_day or "阴" in self.w_day:
            return "☁️"

    def __str__(self) -> str:
        d_str = f"{self.w_day}{self.w_day_emoji}({self.temp_min}°~{self.temp_max}°)"

        if self.w_night != self.w_day:
            d_str += f"，夜晚{self.w_night}"

        if self.temp_now:
            d_str += f"，现在{self.temp_now}°C"

        if self.air_aqi and self.air_text:
            d_str += f"，空气质量{self.air_text}({self.air_aqi})"

        return d_str
