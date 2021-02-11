from aiogram import Dispatcher, Bot

from telegram_bot.telegram.dispatcher import dp


def bot_dispatcher() -> Dispatcher:
    """
    Set context manually for properly processing webhook updates.
    """
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    return dp


def telegram_bot() -> Bot:
    return dp.bot
