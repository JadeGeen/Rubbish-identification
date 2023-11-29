import flask
import base64
import logging
import traceback
import numpy as np
import json
import requests
from flask import Flask, request
from concurrent.futures import ProcessPoolExecutor

from api import api

app = Flask(__name__)
base = None
target = None
contra = False
pool = ProcessPoolExecutor(2)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def Judge(target, base = None):
    if base == None and type(target) == np.ndarray:
        return 'Upload successfully'
    elif type(base) == np.ndarray and type(target) == np.ndarray:
        return 'Upload successfully'
    return 'Upload failed'

@app.route('/')
def hello():
    return 'This is algorithm server'

@app.route('/upload', methods = ['POST'])
def upload():
    res = {"target" : [], "res" : {}}
    if flask.request.method == "POST":

        try:
            data = flask.request.json

            contra = data["contra"]
            contra = base64.b64decode(contra.encode('ascii'))
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
            
        except Exception as e:
            logger.warning(f'{e}')
            logger.warning(traceback.print_exc())

    return flask.jsonify(res)

if __name__ == '__main__':
    logger.info(f"server is running")
    app.run()