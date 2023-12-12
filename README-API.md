# API定义

## APP FOR USER

```python
@app.route('/user-login', methods=['POST'])
input:{
    "url": str,
    "userID": str,
    "white":str, # 摄像头白名单，用','隔开
    "black":str# 黑名单，同上
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

@app.route('/user-wblist_change', methods=['POST'])
input:{
    "userID": str,
    "label":, # 要进行操作的标签
    "wb":int, #0 为对白名单进行操作,1为对黑名单进行操作
    "tag":bool, # 操作类型,True为添加,False为删除
    ...
}
output:{
    ...
}

@app.route('/user-clear', methods=['POST'])
input:{
    "userID": str,
    "time_msg": str
    ...
}
output:{
    ...
}
```

## APP FOR ALG

```python
@alg.route('/app-postPic', methods=['POST'])
input:{
    "userID":str,
    "time_msg":str,
    "bboxs_list":dict,
    "target":ndarray,
    ...
}
output:{
    ...
}

```
