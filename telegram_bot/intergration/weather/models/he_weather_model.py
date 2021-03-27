from dataclasses import dataclass


@dataclass
class HeWeatherModel:
    w_day: str
    w_night: str

    temp_min: str
    temp_max: str
    temp_now: str

    def __str__(self) -> str:
        d_str = f"白天{self.w_day}({self.temp_min}°~{self.temp_max}°)"

        if self.temp_now:
            d_str += f"，当前气温{self.temp_now}°C"

        if self.w_night != self.w_day:
            d_str += f"，夜晚{self.w_night}"

        return d_str
