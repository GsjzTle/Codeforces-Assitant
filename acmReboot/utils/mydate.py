import time
from datetime import datetime, timedelta


# 获取星期一的时间戳
def getMonday():
    now_date = datetime.now().date()  # 获取当前日期
    now_week = now_date.weekday()  # 获取当前日期的星期
    monday_date = now_date - timedelta(days=now_week)  # 计算当前日期所在周的周一,默认h = m = s = 0
    return time.mktime(monday_date.timetuple())  # timetuple 会把日期转换为 (y,m,d,h,s,...) 元组


# 将时间戳转换为日期形式
def formatDate(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


#  将秒转换为时分秒
def formatSeconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    day, h = divmod(h, 24)
    if day > 0:
        return "%d天%02d:%02d:%02d" % (day, h, m, s)
    return "%02d:%02d:%02d" % (h, m, s)
