from sqlalchemy.orm import Session

from telegram_bot.database import models
from telegram_bot.intergration.location.he_location_client import Location


def get_user(db: Session, chat_id: str):
    return db.query(models.User).filter(models.User.chat_id == chat_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_or_create_user(db: Session, chat_id: str, location: Location):
    new_user = models.User(
        chat_id=int(chat_id),
        latitude=location.lat,
        longitude=location.lon,
        city=location.name,
        city_name=location.name,
        time_zone=location.tz
    )

    db_user = db.merge(new_user)

    db.commit()
    db.refresh(db_user)
    return db_user
