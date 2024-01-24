import requests

from Config import config
from Screening_Strategies.api import api_save

# 发送给指定服务器
def send_res(userID, Imgld, time_msg, bbox_list, target):
    res = api_save(userID, time_msg, bbox_list, target)
    allres=res[0]
    for bbox in allres:
        requests.post(
        config['Restarget_addr'],
        data={
            'VideoID': userID,
            'Imgld': Imgld,
            'TargerTime': time_msg,
            'TargetX': bbox[0],
            'TargetY': bbox[1],
            'TargetW': bbox[2],
            'TargetH': bbox[3],
            'TargetD': ' ',
            'Img': res[1],
        },  
    )
