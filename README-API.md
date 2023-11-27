# API定义

## APP FOR USER

```python
@app.route('/user-login', methods=['POST'])
input:{
    "url": str,
    "userID": str,
    ...
}
output:{
    ...
}

@app.route('/user-getRes', methods=['GET'])
input:{
    "userID": str,
    "time_msg": str
    ...
}
output:{
    "res":     # 识别结果，形式待定
    "msg": str # 信息 
    ...
}
```

## APP FOR ALG

```python
@alg.route('/app-postPic', methods=['POST'])
input:{
    "res": json,
    ...
}
output:{
    ...
}

```
