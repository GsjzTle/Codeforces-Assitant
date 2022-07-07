from datetime import datetime
from time import sleep
from utils.mydate import formatDate, getMonday
from codeforces.model import UserSubmission
from codeforces.methods import getUserAcRank, sendGroupAcRank, getContests
from codeforces.tables import mnnu_users_name, mnnu_group_id, test_id

print(getContests())


