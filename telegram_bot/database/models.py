from sqlalchemy import Boolean, Column, Integer, String

from .database import Base
from ..intergration.location.he_location_client import Location


class User(Base):
    __tablename__ = "users"

    chat_id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)

    latitude = Column(String)
    longitude = Column(String)
    city = Column(String, nullable=False)
    city_name = Column(String, nullable=False)

    time_zone = Column(String, nullable=False)

    @property
    def location(self):
        return Location(name=self.city_name, lat=float(self.latitude), lon=float(self.longitude), tz=self.time_zone)
