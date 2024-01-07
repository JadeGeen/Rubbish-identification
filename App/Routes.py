from flask import Flask, request
import json
import threading

from Config import config
from Screening_Strategies.api import api_search, api_clear, api_wblist_change
from Fileprocess import fileprocess
from Utils import send_res

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user-login', methods=['POST'])
def login():
    data = json.loads(str(request.data, 'utf-8'))
    userID = str(data['userID'])
    url = str(data['url'])
    intervalSEC = int(data['intervalSEC'])
    white = str(data['white'])
    black = str(data['black'])
    # 保存摄像头配置，写入txt
    with open(config['Login_msg'], 'a') as f:
        f.write(
            userID + " " + url + " " + intervalSEC + " " + white + " " + black + "\n"
        )
    # 每个摄像头启用一个新线程
    new_th = threading.Thread(target=fileprocess, args=(userID, url, intervalSEC))
    new_th.start()

'''
@app.route('/user-getRes', methods=['GET'])
def get_Res():
    data = json.loads(str(request.data, 'utf-8'))
    userID = int(data['userID'])
    time_msg = data['time_msg']
    res = api_search(userID, time_msg)
    if res:
        return res
    else:
        msg = '<h1>FileID:' + str(userID) + 'Not done yet.</h1>'
        return msg
'''

@app.route('/user-wblist_change', method=['POST'])
def wblist_change():
    data = json.loads(str(request.data, 'utf-8'))
    userID = int(data['userID'])
    label = data['label']
    wb = int(data['wb'])
    tag = bool(data['tag'])
    api_wblist_change(userID, label, wb, tag)


@app.route('/user-clear', methods=['POST'])
def clear():
    data = json.loads(str(request.data, 'utf-8'))
    userID = int(data['userID'])
    time_msg = data['time_msg']
    api_clear(userID, time_msg)


@app.route('/alg-postPic', methods=['POST'])
def post_Pic():
    data = json.loads(str(request.data, 'utf-8'))
    strategy = threading.Thread(
        target=send_res,
        args=(
            data['userID'],
            data['ImgID'],
            data['time_msg'],
            data['bboxs_list'],
            data['target'],
        ),
    )
    strategy.start()
    return "<h1>Using strategy</h1>"


def app_RUN():
    app.run()
