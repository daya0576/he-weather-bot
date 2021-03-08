from typing import List

from sqlalchemy.orm import Session

from telegram_bot.database import models
from telegram_bot.intergration.location.he_location_client import Location


def get_user(db: Session, chat_id: str) -> models.Chat:
    return db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()


def update_user_status(db: Session, chat_id: str, is_active: bool):
    user = db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    if user:
        user.is_active = is_active
        db.merge(user)
    db.commit()

    return user


def get_users(db: Session, skip: int = 0, limit: int = 1000) -> List[models.Chat]:
    return db.query(models.Chat) \
        .offset(skip).limit(limit).all()


def update_or_create_user(db: Session, chat_id: str, location: Location) -> models.Chat:
    new_user = models.Chat(
        chat_id=int(chat_id),
        latitude="{:.2f}".format(location.lat),
        longitude="{:.2f}".format(location.lon),
        city=location.name,
        city_name=location.name,
        time_zone=location.tz
    )

    db_user = db.merge(new_user)

    db.commit()
    db.refresh(db_user)
    return db_user
