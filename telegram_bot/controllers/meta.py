from fastapi import Depends, APIRouter
from loguru import logger
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from telegram_bot.database import crud
from telegram_bot.database.database import get_db, get_db_session
from telegram_bot.settings import aio_lru_cache_1h, settings

router = APIRouter()


@aio_lru_cache_1h
async def get_user_count(db):
    return crud.get_user_count(db)


@router.get("/users/count")
async def active_users_count(db: Session = Depends(get_db)):
    """活跃用户总数"""
    badge_url = f"https://img.shields.io/badge/users-{await get_user_count(db)}-blue"
    return RedirectResponse(badge_url)


@router.get("/")
async def index():
    return "hello"


@router.get("/config")
async def config():
    logger.info(settings)
    return "OK"


@router.get("/sentry")
async def test_sentry():
    return 1 / 0


@router.get("/users")
async def users():
    with get_db_session() as db:
        return crud.get_users(db)


@router.get("/user_count")
async def user_count():
    with get_db_session() as db:
        return await get_user_count(db)
