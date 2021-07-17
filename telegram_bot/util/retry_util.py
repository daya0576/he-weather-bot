import asyncio

from loguru import logger

from telegram_bot.util.exceptions import TooManyTriesException


def tries(times, delay=1, backoff=2):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for time in range(times):
                if time >= 1:
                    time_to_sleep = delay * (backoff ** time)
                    logger.info(f'retry in {time_to_sleep} seconds..')
                    await asyncio.sleep(time_to_sleep)

                try:
                    return await f(*args, **kwargs)
                except Exception as exc:
                    pass
            raise TooManyTriesException() from exc

        return wrapper

    return func_wrapper
