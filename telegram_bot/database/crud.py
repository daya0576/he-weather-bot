from typing import Iterable, List

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, make_transient

from telegram_bot.database import models
from telegram_bot.intergration.location.he_location_client import Location


def is_user_exists(db: Session, chat_id: str) -> bool:
    return (
        db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first() is not None
    )


def get_user(db: Session, chat_id: str) -> models.Chat:
    return (
        db.query(models.Chat)
        .options(joinedload(models.Chat.api_key))
        .filter(models.Chat.chat_id == chat_id)
        .first()
    )


def get_user_locations(db: Session, chat_id: str) -> Iterable[Location]:
    chat = get_user(db, chat_id)
    if not chat:
        return []
    yield chat.location

    locations = filter_locations(db, chat_id)
    yield from [x.location for x in locations]


def get_active_users(
    db: Session, skip: int = 0, limit: int = 100000
) -> List[models.Chat]:
    return (
        db.query(models.Chat)
        .options(joinedload(models.Chat.api_key))
        .filter(models.Chat.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_count(db: Session) -> int:
    return db.query(func.count(models.Chat.chat_id)).scalar()


def update_user_status(db: Session, chat_id: str, is_active: bool):
    user = db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    if user:
        user.is_active = is_active
        db.merge(user)
    db.commit()


def update_location_name(db: Session, chat_id: str, location_name: str) -> None:
    chat = db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    if chat:
        chat.city_name = location_name
        chat.city = location_name
        db.merge(chat)
    db.commit()


def migrate_user_by_chat_id(db: Session, chat_id: str, new_chat_id: str):
    user: models.Chat = (
        db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    )
    if not user:
        raise Exception(f"chat_id does not exist: {chat_id}!!")

    db.expunge(user)
    make_transient(user)
    user.chat_id = new_chat_id
    db.add(user)

    # 复制订阅的定时任务
    cron_job_list = (
        db.query(models.CronJobs).filter(models.CronJobs.chat_id == chat_id).all()
    )
    for cron_job in cron_job_list:
        db.expunge(cron_job)
        make_transient(cron_job)
        cron_job.chat_id = new_chat_id
        cron_job.id = None
        db.add(cron_job)

    db.commit()


def update_or_create_user_by_location(
    db: Session, chat_id: str, location: Location
) -> models.Chat:
    chat = models.Chat(
        chat_id=int(chat_id),
        latitude="{:.2f}".format(location.lat),
        longitude="{:.2f}".format(location.lon),
        city=location.name,
        city_name=location.name,
        time_zone=location.tz,
    )

    if db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first():
        # update
        chat = db.merge(chat)
    else:
        # create
        chat.is_active = True
        db.add(chat)

    db.commit()
    db.refresh(chat)
    return chat


def add_location(db: Session, chat_id: str, location: Location) -> models.Chat:
    sub_location = models.Locations(
        chat_id=int(chat_id),
        latitude="{:.2f}".format(location.lat),
        longitude="{:.2f}".format(location.lon),
        city=location.name,
        city_name=location.name,
        time_zone=location.tz,
    )
    db.add(sub_location)
    db.commit()
    db.refresh(sub_location)
    return sub_location


def filter_locations(db: Session, chat_id: str) -> List[models.Locations]:
    return db.query(models.Locations).filter(models.Locations.chat_id == chat_id).all()


def get_ding_bot(db: Session, chat_id: str) -> models.DingBots:
    chat = get_user(db, chat_id)
    return chat.ding_bot


def update_or_create_ding_bot(db: Session, chat_id: str, ding_token: str):
    ding_bot = get_ding_bot(db, chat_id)
    if ding_bot:
        # update
        ding_bot.token = ding_token
        db.merge(ding_bot)
    else:
        # create
        ding_bot = models.DingBots(token=ding_token, chat_id=chat_id)
        db.add(ding_bot)

    db.commit()


def remove_ding_bot(db: Session, chat_id: str):
    dingbot = (
        db.query(models.DingBots).filter(models.DingBots.chat_id == chat_id).first()
    )

    if dingbot:
        db.delete(dingbot)
        db.commit()
        return True
    return False


def remove_sub_location(db: Session, location_id: str) -> bool:
    location = (
        db.query(models.Locations).filter(models.Locations.id == location_id).first()
    )
    if location:
        db.delete(location)
        db.commit()
        return True
    return False


def get_cron_job(db, chat_id, hour):
    return (
        db.query(models.CronJobs)
        .filter(models.CronJobs.chat_id == chat_id)
        .filter(models.CronJobs.hour == hour)
        .first()
    )


def create_or_delete_cron_job(db: Session, chat_id: int, hour: str):
    cron_job = (
        db.query(models.CronJobs)
        .filter(models.CronJobs.chat_id == chat_id)
        .filter(models.CronJobs.hour == hour)
        .first()
    )

    if cron_job:
        db.delete(cron_job)
        created = False
    else:
        cron_job_to_create = models.CronJobs(chat_id=chat_id, hour=hour)
        db.add(cron_job_to_create)
        created = True

    db.commit()

    return cron_job, created


def get_active_cron_jobs_by_hour(db: Session, hour: str):
    return (
        db.query(models.CronJobs)
        .filter(models.CronJobs.hour == hour)
        .filter(models.CronJobs.parent.is_active is True)
        .all()
    )


def get_api_key(db: Session, chat_id: str) -> models.ApiKey:
    return db.query(models.ApiKey).filter(models.ApiKey.chat_id == chat_id).first()


def update_or_create_api_key(db: Session, chat_id: str, host: str, key: str):
    api_key = get_api_key(db, chat_id)
    if api_key:
        # update
        api_key.host = host
        api_key.key = key
        db.merge(api_key)
    else:
        # create
        api_key = models.ApiKey(chat_id=chat_id, key=key, host=host)
        db.add(api_key)

    db.commit()
    return api_key


def is_user_api_key_exists(db: Session, chat_id: str) -> bool:
    return (
        db.query(models.ApiKey).filter(models.ApiKey.chat_id == chat_id).first()
        is not None
    )
