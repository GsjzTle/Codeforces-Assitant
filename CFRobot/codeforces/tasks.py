import threading
import schedule
from codeforces.tables import mnnu_group_id, mnnu_users_name, test_id

from codeforces.methods import sendAT, sendGroupRatingRank, sendGroupAcRank, sendGroupContests


def run_thread(job_func, group_id, user_name=None):
    job_thread = threading.Thread(target=job_func, args=(group_id, user_name))
    job_thread.start()


def sendRank(group_id, user_name):
    sendGroupRatingRank(group_id, user_name)


def sendAC(group_id, user_name):
    sendGroupAcRank(group_id, user_name)


def sendContest(group_id):
    sendGroupContests(group_id)


def AllTask(group_id, user_name):
    sendGroupRatingRank(group_id, user_name)
    sendGroupAcRank(group_id, user_name, False)
    sendGroupContests(group_id, False)


def Task():
    schedule.every().thursday.at("12:00").do(run_thread, AllTask, test_id, mnnu_users_name)
    schedule.every().sunday.at("12:00").do(run_thread, AllTask, test_id, mnnu_users_name)
