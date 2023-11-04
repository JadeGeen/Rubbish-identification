from flask import Flask, request
import json
import requests

from Utils import get_pic_number, movie_downdload
from Fileprocess import fileprocess
from Screening_Strategies.Strategies import screening_startegies


Alg_addr = ''

movie_ID = 0
app = Flask(__name__)


'''
均存在嵌套请求的问题；
考虑使用脚本拆解，即不通过客户（对调度）的请求触发调度（对算法）的请求；
考虑使用数据库存储数据。
'''


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user-uploadfile', methods=['POST'])
def uploadfile():
    data = json.loads(str(request.data, 'utf-8'))
    url = str(data['url'])
    fileID = movie_ID
    movie_downdload(url, fileID)
    movie_ID += 1

    pic_list = fileprocess(fileID)
    requests.post(Alg_addr+'/app-uploadfile', data={"pic_list":pic_list})

    return fileID


@app.route('/user-getRes', methods=['GET'])
def get_Res():
    data = json.loads(str(request.data, 'utf-8'))
    fileID = str(data['fileID'])
    pic_number = get_pic_number(fileID)

    pic_processed = []
    for i in range(pic_number):
        pic = requests.get(Alg_addr+'/app-getRes',data={"fileID":fileID})
        if pic:
            pic_processed.append(pic)

    if len(pic_processed) == pic_number:
        res = screening_startegies(pic_processed)
        requests.post(Alg_addr+'/delete-data', data={"fileID":fileID})
        return res
    else:
        msg = 'FileID:' + str(fileID) + 'Not completed yet.'
        return msg
