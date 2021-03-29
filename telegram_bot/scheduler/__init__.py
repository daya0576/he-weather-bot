from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from pytz import utc
from sentry_sdk import capture_exception

from telegram_bot.settings import redis_config

jobstores = {
    'default': RedisJobStore(host=redis_config.host, port=redis_config.port, password=redis_config.password)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {}


def my_listener(event: JobExecutionEvent):
    if event.exception:
        capture_exception(event.exception)
        logger.exception(event.exception, 'The job crashed :(')
    else:
        logger.info('The job worked :)')


scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
