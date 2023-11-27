from flask import Flask, request

import numpy as np
import json
import requests
from concurrent.futures import ProcessPoolExecutor


from api import api

app = Flask(__name__)
base = None
target = None
contra = False

pool = ProcessPoolExecutor(2)

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
    data = json.loads(str(request.data, 'utf-8'))
    contra = data[contra]
    if contra:
        base = data[base]
        target = data[target]
    else:
        target = data[target]
    str = pool.submit(Judge, args = (target, base) if contra else (target))
    return str

data = pool.submit(api, (target, contra, base) if contra else (target, contra))

@app.route('/download', metheds = ['GET'])
def download():
    res = json.dumps(data)
    return res

if __name__ == '__main__':
    app.run()