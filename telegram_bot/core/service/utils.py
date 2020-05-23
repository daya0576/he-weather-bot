# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytz


def get_tomorrow_day():
    d = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}

    tz = pytz.timezone('Asia/Shanghai')
    cur_time = datetime.now(tz) + timedelta(days=1)
    return d[cur_time.weekday()]
