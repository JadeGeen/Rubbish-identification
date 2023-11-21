from flask import Flask, request
import json
import requests

from api import api

app = Flask(__name__)
base = None
target = None
contra = False

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
    return 'Upload successfully'

@app.route('/download', metheds = ['GET'])
def download():
    res = api(target, contra, base) if contra else api(target, contra)
    return res

if __name__ == '__main__':
    app.run()