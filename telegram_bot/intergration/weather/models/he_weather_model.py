from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HeWeatherModel:
    w_day: str
    w_night: str

    temp_min: str
    temp_max: str
    temp_now: str

    air_aqi: str
    air_text: str

    life_text: str
    warning_text: str

    @classmethod
    def build(cls, weather_daily: Dict, weather_now: Dict = None, air_now: Dict = None, indices: List = None,
              warning: List = None):
        weather_now = weather_now or {}
        air_now = air_now or {}
        indices_d1 = indices[0] if indices else {}
        warning_first = warning[0] if warning else {}
        return cls(
            weather_daily.get("textDay", ""),
            weather_daily.get("textNight", ""),
            weather_daily.get("tempMin", ""),
            weather_daily.get("tempMax", ""),
            weather_now.get("temp", ""),
            air_now.get("aqi", ""),
            air_now.get("category", ""),
            indices_d1.get("text", ""),
            warning_first.get("text", ""),
        )

    @staticmethod
    def with_emoji(day_text):
        emoji_map = {"晴": "☀️", "晴间多云": "🌤", "雷阵雨": "⛈"}
        if emoji := emoji_map.get(day_text):
            return emoji

        if "雪" in day_text:
            return "❄️"
        if "雨" in day_text:
            return "🌧"
        if "云" in day_text or "阴" in day_text:
            return "☁️"

        return ""

    @property
    def w_day_with_emoji(self):
        return f"{self.with_emoji(self.w_day)}{self.w_day}"

    @property
    def w_night_with_emoji(self):
        return self.w_night + self.with_emoji(self.w_night)

    def __str__(self) -> str:
        d_str = f"{self.w_day_with_emoji}"

        if self.temp_min and self.temp_max:
            d_str += f"({self.temp_min}°~{self.temp_max}°)"

        if self.w_night != self.w_day:
            d_str += f"，夜间{self.w_night}"
        if self.air_aqi and self.air_text:
            d_str += f"，空气{self.air_text}({self.air_aqi})"

        return d_str
