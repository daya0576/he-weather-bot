from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    is_active = Column(Boolean, default=True)

    latitude = Column(Integer)
    longitude = Column(Integer)
    city = Column(String)
