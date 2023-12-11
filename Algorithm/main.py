import flask
import base64
import logging
import traceback
import json
import requests
from flask import Flask, request

from api import api

SERVER_URL = "0.0.0" #调度服务器url

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

@app.route('/')
def hello():
    return 'This is algorithm server'

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    res = {"target" : [], "res" : {}}
    if request.method == "POST":

        try:
            data = request.json

            contra = data["contra"]
            if contra:
                base = data["base"]
                base = base64.b64decode(base.encode('ascii'))
                target = data["target"]
                target = base64.b64decode(target.encode('ascii'))
                info = api(target, contra, base)
            else:
                target = data["target"]
                target = base64.b64decode(target.encode('ascii'))
                info = api(target, contra)
            res['target'] = target
            info = base64.b64encode(bytes).decode()
            res['res'] = info
            requests.post(url = SERVER_URL, data = json.dumps(res),)
            
        except Exception as e:
            logger.warning(f'{e}')
            logger.warning(traceback.print_exc())

    return flask.jsonify(res)

if __name__ == '__main__':
    logger.info(f"server is running")
    app.run()