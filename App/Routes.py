from flask import Flask, request
import json

from Utils import send_Pic
from Screening_Strategies.api import api_search

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user-login', methods=['POST'])
def login():
    data = json.loads(str(request.data, 'utf-8'))
    userID = str(data['userID'])
    url = str(data['url'])
    # TODO: 保存摄像头配置文件, 形式待定


@app.route('/user-getRes', methods=['GET'])
def get_Res():
    data = json.loads(str(request.data, 'utf-8'))
    userID = int(data['userID'])
    time = data['time']
    # TODO: add more needed args
    res = api_search(userID, time)
    if res:
        return res
    else:
        msg = 'FileID:' + str(userID) + 'Not done yet.'
        return msg


@app.route('/alg-postPic', methods=['POST'])
def post_Pic():
    data = json.loads(str(request.data, 'utf-8'))
    send_Pic(data['res'])


def app_RUN():
    app.run()
