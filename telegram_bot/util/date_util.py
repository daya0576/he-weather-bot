# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytz


class DateUtil:
    @staticmethod
    def get_day(time_zone, day=1):
        d = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}

        tz = pytz.timezone(time_zone)
        cur_time = datetime.now(tz) + timedelta(days=day)
        return d[cur_time.weekday()]

    @staticmethod
    def get_cur_hour(time_zone: str = 'UTC') -> str:
        tz = pytz.timezone(time_zone)
        return str(datetime.now(tz).hour)
