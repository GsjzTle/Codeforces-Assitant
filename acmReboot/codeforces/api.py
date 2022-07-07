from flask import Flask, request
from codeforces.tables import mnnu_group_id, mnnu_users_name
from codeforces.methods import sendGroupRatingRank, sendPrivateRatingRank, sendGroupAcRank, \
    sendPrivateAcRank, sendPrivateContests, sendGroupContests

app = Flask(__name__)


@app.route("/ha", methods=['GET', 'POST'])
def hello_world():
    print(request)
    return "<p>Hello, World!</p>"


@app.route('/', methods=["POST"])
def post_data():
    if request.get_json().get("message_type") == "private":  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        if message == "CF排名" or message == "cf排名":
            sendPrivateRatingRank(uid, mnnu_users_name)
        if message == "AC排名" or message == "ac排名" or message == "Ac排名" or message == "aC排名":
            sendPrivateAcRank(uid, mnnu_users_name)
        if message == "cf比赛" or message == "CF比赛":
            sendPrivateContests(uid)
    if request.get_json().get('message_type') == 'group':  # 如果是群聊信息
        gid = request.get_json().get('group_id')  # 获取群号
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        if message == "CF排名" or message == "cf排名":
            sendGroupRatingRank(gid, mnnu_users_name, uid)
        if message == "AC排名" or message == "ac排名" or message == "Ac排名" or message == "aC排名":
            sendGroupAcRank(gid, mnnu_users_name, uid)
        if message == "cf比赛" or message == "CF比赛":
            sendGroupContests(gid, uid)
    return "OK"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5705)  # 监听

