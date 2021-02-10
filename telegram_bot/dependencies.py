from aiogram import Dispatcher, Bot

from telegram_bot.telegram.dispatcher import dispatcher


def bot_dispatcher() -> Dispatcher:
    """
    Set context manually for properly processing webhook updates.
    """
    Bot.set_current(dispatcher.bot)
    Dispatcher.set_current(dispatcher)
    return dispatcher


def telegram_bot() -> Bot:
    return dispatcher.bot
