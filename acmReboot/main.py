import schedule
from codeforces.tasks import Task
from codeforces.api import app

Task()
while True:
    schedule.run_pending()

# import time
# from datetime import datetime, timedelta
#
# now_date = datetime.now().date()  # 获取当前日期
# now_week = now_date.weekday()  # 获取当前日期的星期
#
# monday_date = now_date - timedelta(days=now_week)  # 计算当前日期所在周的周一,默认 h = m = s = 0
# monday_stamp = monday_date.timetuple()
# print(time.mktime(monday_date.timetuple()))
