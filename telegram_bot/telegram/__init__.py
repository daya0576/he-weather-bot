""" manually import to be reachable """
from telegram_bot.telegram import (
    callbacks,
    update_location,
    add_location,
    update_dingbot,
    exception,
)

__all__ = [
    "bot",
    "dispatcher",
]
