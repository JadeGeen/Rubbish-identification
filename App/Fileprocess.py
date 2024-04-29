import cv2
import requests
import time
from datetime import datetime

from Config import config

test_save_path = r'./Data'


# 切帧
def frame_cut(url):
    video = cv2.VideoCapture(url)
    ret, pic = video.read()
    cut_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.imencode('.jpg', pic)[1].tofile(test_save_path + "/test.jpg")
    video.release()
    return pic, cut_time


# 间隔时间切帧
def fileprocess(ID, url, sec):
    Imgld = 0
    while 1:
        pic, cut_time = frame_cut(url)
        requests.post(
            config['Alg_addr'] + '/upload',
            data={
                'target': pic,
                'contra': False,
                'userID': ID,
                'Imgld': Imgld,
                'time_msg': cut_time,
            },
        )
        time.sleep(sec)


# 本地视频单图测试
def local_single_test(ID, url):
    pic, cut_time = frame_cut(url)

    requests.post(
        config['Alg_addr'] + '/upload',
        data={
            'target': pic,
            'contra': False,
            'userID': ID,
            'Imgld': 0,
            'time_msg': cut_time,
        },
    )


# 单视频单图测试
def time_cut(ID):
    r = requests.post(config['Getjs_addr'])
    data = r.json()
    js = data['jsession']
    print("Conversation ID(jsession):" + str(js))

    url = config['Getvideo_addr_L'] + js + config['Getvideo_addr_R']
    r2 = requests.post(url)
    r2 = r2.json()
    print(r2['result'])

    pic, cut_time = frame_cut(url)
    requests.post(
        config['Alg_addr'] + '/upload',
        data={
            'target': pic,
            'contra': False,
            'Imgld': 0,
            'time_msg': cut_time,
            'userID': ID
        },
    )

    '''
    video = cv2.VideoCapture(url)
    while True:
        ret, frame = video.read()
        FPS = video.get(5)
        if ret:
            frameRate = int(FPS) * time
            if c % frameRate == 0:
                print("cut:" + str(c))
                cv2.imwrite("./capture_image/" + str(c) + '.jpg', frame)
            c += 1
            cv2.waitKey(0)
        else:
            print("所有帧都已经保存完成")
            break    
    '''
