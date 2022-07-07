from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from datetime import datetime
from codeforces.tables import rating_color, AC_Rank_Time, Rating_Rank_time
from utils.mydate import getMonday, formatDate, formatSeconds
from codeforces.model import UserSubmission

url_reboot = "http://127.0.0.1:5700"
url_cf = "http://codeforces.com/api"

RES = requests.session()
RES.mount('http://', HTTPAdapter(max_retries=Retry(total=5)))
RES.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
}


# 获取 rating 排名
def getUserRatingRank(user_name):
    handles = ""
    for handle in user_name.keys():  # 取出 key 值（用户名）
        handles = handles + handle + ";"
    params = {
        "handles": handles
    }
    response = RES.get(url=url_cf + "/user.info", params=params)
    while response.status_code != 200:
        response = RES.get(url=url_cf + "/user.info", params=params)
    res = response.json().get("result")
    users = []
    for i in range(0, len(res)):
        user = (user_name[res[i].get("handle").lower()],  # 真实姓名
                res[i].get("handle"),  # 用户名
                0 if res[i].get("rating") is None else res[i].get("rating"),  # 分数
                rating_color[res[i].get("rank")])  # 颜色
        users.append(user)
    users.sort(key=lambda x: (x[2]), reverse=True)
    message = "\t《MNNU Codeforces 排名》\t\t\n"
    for i in range(0, len(users)):
        message = message + "NO." + str(i + 1) + " :\t\n 	name   :  " \
                  + users[i][0] + "     \t\n 	handle :  " \
                  + users[i][1] + "     \t\n 	rating   :  " \
                  + str(users[i][2]) + "(" + users[i][3] + ")     \t\n\n"
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message


# 刷题排行榜
def getUserAcRank(user_name):
    users = []
    monday_stamp = getMonday()
    for handle in user_name.keys():
        params = {
            "handle": handle,
            "from": "1",
            "count": "100",
        }
        response = RES.get(url=url_cf + "/user.status", params=params, headers=headers)
        # 不断尝试直到请求成功
        print(handle)
        while response.status_code != 200:
            sleep(1.2)
            response = RES.get(url=url_cf + "/user.status", params=params, headers=headers)
        res = response.json().get("result")
        ac_number = 0  # 总数过题数
        total = 0  # 总提交数
        problem_list = []  # 过题列表
        for j in res:
            timestamp = j.get("creationTimeSeconds")  # 获取提交时间戳
            if timestamp < monday_stamp:  # 如果是上周的提交，则忽略
                break
            if j.get("verdict") != "OK":  # 只统计正确代码
                total += 1
                continue
            total += 1
            ac_number += 1
            contest_id = j.get("contestId")
            problem_index = j.get("problem").get("index")  # 题目编号对应的字母：A、B、C...
            problem_name = j.get("problem").get("name")
            problem_score = j.get("problem").get("rating")  # 题目难度分值
            if problem_score is None:
                problem_score = "???"
            problem = {
                "pname": "Codeforces " + str(contest_id) + problem_index + " " + problem_name,
                "pscore": problem_score,
                "pass_time": formatDate(timestamp)
            }
            problem_list.append(problem)
        # user = UserSubmission(user_name[handle.lower()], handle, ac_number, total, problem_list)
        # print(user.to_String())
        users.append(UserSubmission(user_name[handle.lower()], handle, ac_number, total, problem_list))
    users.sort(reverse=True)
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = "\t\t  《本周 Codeforces AC榜》\n"
    message = message + "更新时间 : " + now_time + "\n"
    messages = []
    for i in range(len(users)):
        now_info = " =================== NO." + str(i + 1) + "===================\n" + users[i].to_String()
        if len(message) + len(now_info) > 3500:
            messages.append(message)
            message = now_info
        else:
            message += " =================== NO." + str(i + 1) + "===================\n" + users[i].to_String()
    if message != "":
        messages.append(message)
    return messages


# 获取即将开始的比赛信息
def getContests():
    response = RES.get(url=url_cf + "/contest.list")
    while response.status_code != 200:
        response = RES.get(url=url_cf + "/contest.list")
        sleep(0.3)
    res = response.json().get("result")
    contests = []
    for i in res:
        if i.get("phase") == "FINISHED":
            break
        contest = {
            "name": i.get("name"),
            "begin_time": formatDate(i.get("startTimeSeconds")),
            "end_time": formatDate(i.get("startTimeSeconds") + i.get("durationSeconds")),
            "type": i.get("type"),
            "status": i.get("phase"),
            "relative_time": i.get("relativeTimeSeconds")
        }
        contests.append(contest)
    message = "比赛日历 : "
    if len(contests) == 0:
        message += "[空空如也]\t\t\n\n"
        return message
    message += "\t\t\n[\n"
    for i in contests[::-1]:
        message += " 	比赛名称 : " + i["name"] + "     \n" \
                   + " 	开始时间 : " + i["begin_time"] + "     \t\n" \
                   + " 	结束时间 : " + i["end_time"] + "     \t\n" \
                   + " 	比赛类型 : " + i["type"] + "     \t\n"
        if i["status"] != "BEFORE":
            message += " 	比赛状态 : 进行中...\t\n\n"
        else:
            message += " 	比赛状态 : 未开始，距开始剩余 " + formatSeconds(abs(i["relative_time"])) + "\t\n\n"
    message += "]\n"
    now_time = datetime.now()
    now_time = datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
    message = message + "更新时间 : " + now_time
    return message


# 发送 rating 排名至 QQ 群
def sendGroupRatingRank(group_id, user_name, u_id=None, flag=True):
    message = getUserRatingRank(user_name)
    data = {
        "group_id": group_id,
        "message": message
    }
    # sleep(Rating_Rank_time)  # 等待获取数据
    sendAT(group_id, u_id, flag)
    requests.post(url=url_reboot + "/send_group_msg", json=data)


# 发送 rating 排名（私聊）
def sendPrivateRatingRank(uid, user_name):
    data = {
        "user_id": uid,
        "message": getUserRatingRank(user_name)
    }
    requests.post(url=url_reboot + "/send_private_msg", json=data)


def sendGroup(group_id, message):
    data = {
        "group_id": group_id,
        "message": message
    }
    requests.post(url=url_reboot + "/send_group_msg", json=data)


# 发送ac排名至 QQ 群
def sendGroupAcRank(group_id, user_name, u_id=None, flag=True):
    messages = getUserAcRank(user_name)
    sendAT(group_id, u_id, flag)
    for i in messages:
        data = {
            "group_id": group_id,
            "message": i
        }
        requests.post(url=url_reboot + "/send_group_msg", json=data)
        sleep(0.2)


# 发送ac排名（私聊）
def sendPrivateAcRank(uid, user_name):
    messages = getUserAcRank(user_name)
    for i in messages:
        data = {
            "user_id": uid,
            "message": i
        }
        requests.post(url=url_reboot + "/send_private_msg", json=data)
        sleep(0.2)


# 发送比赛日历至 QQ 群
def sendGroupContests(group_id, u_id=None, flag=True):
    message = getContests()
    data = {
        "group_id": group_id,
        "message": message
    }
    sendAT(group_id, u_id, flag)
    requests.post(url=url_reboot + "/send_group_msg", json=data)


# 发送比赛日历（私聊）
def sendPrivateContests(uid):
    message = getContests()
    data = {
        "user_id": uid,
        "message": message
    }
    requests.post(url=url_reboot + "/send_private_msg", json=data)


# 艾特成员
def sendAT(group_id, u_id, flag=True):
    if not flag:
        pass
    if u_id is None:
        message = "[CQ:at,qq=all]"
    else:
        message = "[CQ:at,qq=" + str(u_id) + ",name=不存在此人]"
    data = {
        "group_id": group_id,
        "message": message,
    }
    requests.post(url=url_reboot + "/send_group_msg", json=data)
