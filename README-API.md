# API定义

## APP FOR USER

```python
@app.route('/user-uploadfile', methods=['POST'])
input:{
    "url": str,
}
output:{
    "fileID": str, # 视频编号
}

@app.route('/user-getRes', methods=['GET'])
input:{
    "fileID": str,
}
output:{
    "res":     # 识别结果，形式待定
    "msg": str # 信息 
}
```

## ALG FOR APP

```python
@alg.route('/app-uploadfile', methods=['POST'])
input:{
    "url": str,
}
output:{
    "fileID": str, # 视频编号
}

@alg.route('/app-getRes', methods=['GET'])
input:{
    "fileID": str,
}
output:{
    "res": json, # 算法输出结果，不存在时为空
}

@alg.route('/delete-data', methods=['POST'])
input:{
    "fileID": str,
}
output:{
    "state": int, # 0成功1失败
}
```
