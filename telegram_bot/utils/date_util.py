# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytz


class DateUtil:
    @staticmethod
    def get_day_of_week(time_zone, day=0):
        """获取未来 N 天的周 X"""
        d = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}

        tz = pytz.timezone(time_zone)
        cur_time = datetime.now(tz) + timedelta(days=day)
        return d[cur_time.weekday()]

    @staticmethod
    def get_cur_hour(time_zone: str = 'UTC') -> int:
        """根据时区获取当前的小时"""
        tz = pytz.timezone(time_zone)
        return datetime.now(tz).hour

    @staticmethod
    def get_now_for_human() -> str:
        tz = pytz.timezone("Asia/Shanghai")
        return datetime.now(tz).strftime("YYYY-MM-DDTHH:MM:SS")
